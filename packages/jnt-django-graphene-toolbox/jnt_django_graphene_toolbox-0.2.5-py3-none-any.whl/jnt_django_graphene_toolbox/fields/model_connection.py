from functools import partial
from typing import Dict, Optional, Type

import django_filters
import graphene
from django.db import models
from graphene import Int, NonNull
from graphene.relay import ConnectionField, PageInfo
from graphene.relay import connection as relay_connection
from graphene_django import settings, utils
from graphql_relay.connection.arrayconnection import (
    connection_from_list_slice,
    cursor_to_offset,
    get_offset_with_default,
    offset_to_cursor,
)
from promise import Promise

from jnt_django_graphene_toolbox.errors import (
    GraphQLInputError,
    GraphQLPermissionDenied,
)
from jnt_django_graphene_toolbox.filters import SortHandler
from jnt_django_graphene_toolbox.types import BaseModelObjectType


class BaseModelConnectionField(ConnectionField):  # noqa: WPS214
    """Base class for model collections."""

    sort_handler: Optional[SortHandler] = None
    filterset_class: Optional[Type[django_filters.FilterSet]] = None
    auth_required: bool = False

    def __init__(self, *args, **kwargs):
        """Initialize."""
        self.on = kwargs.pop("on", False)
        self.max_limit = kwargs.pop(
            "max_limit",
            settings.graphene_settings.RELAY_CONNECTION_MAX_LIMIT,
        )
        self.enforce_first_or_last = kwargs.pop(
            "enforce_first_or_last",
            settings.graphene_settings.RELAY_CONNECTION_ENFORCE_FIRST_OR_LAST,
        )
        kwargs.setdefault("offset", Int())

        if self.sort_handler:
            kwargs["sort"] = graphene.Argument(
                graphene.List(self.sort_handler.enum),
            )

        super().__init__(*args, **kwargs)

    @property
    def type(self):  # noqa: WPS125
        """Returns connection field type."""
        _type = super(  # noqa: WPS122 WPS608
            relay_connection.IterableConnectionField,
            self,
        ).type
        non_null = False
        if isinstance(_type, NonNull):
            _type = _type.of_type  # noqa: WPS122
            non_null = True

        if not issubclass(_type, BaseModelObjectType):
            raise ValueError(
                "BaseModelConnectionField only accepts BaseModelObjectType types",  # noqa: E501
            )

        if not _type._meta.connection:  # noqa: WPS437
            raise ValueError(
                "The type {0} doesn't have a connection".format(
                    _type.__name__,
                ),
            )

        connection_type = _type._meta.connection  # noqa: WPS437
        if non_null:
            return NonNull(connection_type)
        return connection_type

    @property
    def connection_type(self):
        """Return connection type."""
        if isinstance(self.type, NonNull):
            return self.type.of_type
        return self.type

    @property
    def node_type(self):
        """Return node type."""
        return self.connection_type._meta.node  # noqa: WPS437

    @property
    def model(self):
        """Return model."""
        return self.node_type._meta.model  # noqa: WPS437

    @classmethod
    def resolve_queryset(
        cls,
        connection,
        queryset,
        info,  # noqa: WPS110
        args,
    ):  # noqa: C901
        """Filter queryset."""
        queryset = connection._meta.node.get_queryset(  # noqa: WPS437
            queryset,
            info,
        )

        queryset = cls._sort_queryset(queryset, info, args)

        return cls._filter_queryset(queryset, info, args)

    @classmethod
    def resolve_connection(  # noqa: WPS210
        cls,
        connection,
        args,
        iterable,
        max_limit=None,
    ):
        """Resolves connection."""
        # Remove the offset parameter and convert it to an after cursor.
        offset = args.pop("offset", None)
        after = args.get("after")
        if offset:
            if after:
                offset += cursor_to_offset(after) + 1
            # input offset starts at 1 while the graphene offset starts at 0
            args["after"] = offset_to_cursor(offset - 1)

        iterable = utils.maybe_queryset(iterable)

        if isinstance(iterable, models.QuerySet):
            list_length = iterable.count()
        else:
            list_length = len(iterable)
        list_slice_length = (
            min(max_limit, list_length)
            if max_limit is not None
            else list_length
        )

        # If after is higher than list_length, connection_from_list_slice
        # would try to do a negative slicing which makes django throw an
        # AssertionError
        after = min(
            get_offset_with_default(args.get("after"), -1) + 1,
            list_length,
        )

        if max_limit is not None and "first" not in args:
            if "last" in args:
                args["first"] = list_length
                list_slice_length = list_length
            else:
                args["first"] = max_limit

        connection = connection_from_list_slice(
            iterable[after:],
            args,
            slice_start=after,
            list_length=list_length,
            list_slice_length=list_slice_length,
            connection_type=connection,
            edge_type=connection.Edge,
            pageinfo_type=PageInfo,
        )
        connection.iterable = iterable
        connection.length = list_length
        return connection

    @classmethod
    def connection_resolver(  # noqa: C901 WPS211 WPS210 R701 WPS231
        cls,
        resolver,
        connection,
        default_manager,
        queryset_resolver,
        max_limit,
        enforce_first_or_last,
        root,
        info,  # noqa: WPS110
        **args,
    ):
        """Return connection resolver."""
        if cls.auth_required and not info.context.user.is_authenticated:
            return GraphQLPermissionDenied()

        first = args.get("first")
        last = args.get("last")
        offset = args.get("offset")
        before = args.get("before")

        if enforce_first_or_last and not (first or last):
            raise ValueError(
                "You must provide a `first` or `last` value to properly paginate the `{0}` connection.".format(  # noqa: E501
                    info.field_name,
                ),
            )

        if max_limit:
            if first:
                if first > max_limit:
                    raise ValueError(
                        "Requesting {0} records on the `{1}` connection exceeds the `first` limit of {2} records.".format(  # noqa: E501
                            first,
                            info.field_name,
                            max_limit,
                        ),
                    )
                args["first"] = min(first, max_limit)

            if last:
                if last > max_limit:
                    raise ValueError(
                        "Requesting {0} records on the `{1}` connection exceeds the `last` limit of {2} records.".format(  # noqa: E501
                            last,
                            info.field_name,
                            max_limit,
                        ),
                    )
                args["last"] = min(last, max_limit)

        if offset is not None and before is not None:
            raise ValueError(
                "You can't provide a `before` value at the same time as an `offset` value to properly paginate the `{0}` connection.".format(  # noqa: E501
                    info.field_name,
                ),
            )

        # eventually leads to DjangoObjectType's get_queryset (accepts queryset)
        # or a resolve_foo (does not accept queryset)
        iterable = resolver(root, info, **args)
        if iterable is None:
            iterable = default_manager
        # thus the iterable gets refiltered by resolve_queryset
        # but iterable might be promise
        iterable = queryset_resolver(connection, iterable, info, args)
        on_resolve = partial(
            cls.resolve_connection,
            connection,
            args,
            max_limit=max_limit,
        )

        if Promise.is_thenable(iterable):
            return Promise.resolve(iterable).then(on_resolve)

        return on_resolve(iterable)

    def get_resolver(self, parent_resolver):
        """Returns resolver."""
        return partial(
            self.connection_resolver,
            parent_resolver,
            self.connection_type,
            self.get_manager(),
            self.get_queryset_resolver(),  # type: ignore
            self.max_limit,
            self.enforce_first_or_last,
        )

    def get_queryset_resolver(self):
        """Returns queryset resolver."""
        return self.resolve_queryset

    def get_manager(self) -> models.Manager:  # noqa: CCE001
        """Return manager."""
        if self.on:
            return getattr(self.model, self.on)

        return self.model._default_manager  # noqa: WPS437

    @classmethod
    def _filter_queryset(
        cls,
        queryset: models.QuerySet,
        info,  # noqa: WPS110
        args: Dict[str, object],
    ) -> models.QuerySet:
        if not cls.filterset_class:
            return queryset

        filterset = cls.filterset_class(
            data=cls._get_filterset_args(args),
            queryset=queryset,
            request=info.context,
        )
        if not filterset.is_valid():
            raise GraphQLInputError(filterset.errors)

        return filterset.qs

    @classmethod
    def _sort_queryset(
        cls,
        queryset: models.QuerySet,
        info,  # noqa: WPS110
        args: Dict[str, object],
    ) -> models.QuerySet:
        if not cls.sort_handler:
            return queryset

        return cls.sort_handler.filter(queryset, args.get("sort"))

    @classmethod
    def _get_filterset_args(cls, args: Dict[str, object]) -> Dict[str, object]:
        if not cls.filterset_class:
            return {}

        filters_keys = cls.filterset_class.declared_filters.keys()

        return {
            item_key: item_value
            for item_key, item_value in args.items()
            if item_key in filters_keys
        }

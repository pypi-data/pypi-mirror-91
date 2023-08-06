from django.utils.translation import gettext_lazy as _

from jnt_django_graphene_toolbox.errors.base import BaseGraphQLError

NOT_FOUND = "NOT_FOUND"


class GraphQLNotFound(BaseGraphQLError):
    """Not found error."""

    default_message = _("Not found")
    default_extensions = {
        "code": NOT_FOUND,
    }

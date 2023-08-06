from copy import deepcopy
from typing import Dict, Optional

from graphql import GraphQLError


class BaseGraphQLError(GraphQLError):
    """Base class for GraphQL errors."""

    default_message: str = "Error is occurred"
    default_extensions: Optional[Dict[str, str]] = None

    def __init__(self, message=None, extensions=None, *args, **kwargs) -> None:
        """Extending class with default message and extensions."""
        if not message:
            message = self.default_message

        if self.default_extensions:
            merged_extensions = deepcopy(self.default_extensions)
            if extensions:
                merged_extensions.update(extensions)
            extensions = merged_extensions

        kwargs["message"] = message
        kwargs["extensions"] = extensions
        super().__init__(*args, **kwargs)

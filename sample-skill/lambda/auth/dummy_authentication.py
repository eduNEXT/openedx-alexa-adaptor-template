"""Dummy Authentication Backend"""
from auth.base_authentication import BaseEmailAuthenticationBackend


class DummyEmailAuthentication(BaseEmailAuthenticationBackend):
    """
    Dummy Email Authentication Backend

    This authentication backend provides a static email address for demonstration
    purposes. It always returns the same email address.
    """

    def get_email(self) -> str:
        """
        Retrieve the static email address.

        This method always returns the same static email address "john.doe@edunext.co".

        Returns:
            str: The static email address "john.doe@edunext.co".
        """
        return "john.doe@edunext.co"

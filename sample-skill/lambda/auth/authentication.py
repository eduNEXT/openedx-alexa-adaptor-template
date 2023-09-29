"""Authentication Module"""
from auth.base_authentication import BaseEmailAuthenticationBackend


class EmailAuthentication(BaseEmailAuthenticationBackend):
    """
    Email Authentication Backend

    This authentication backend is used to retrieve the user's email address. It
    operates by delegating the email retrieval to a custom backend provided during
    initialization.

    Attributes:
        backend: The custom email authentication backend instance.

    Methods:
        get_email: Retrieve the user's email address using the custom backend.
    """

    def __init__(self, backend) -> None:
        self.backend = backend

    def get_email(self) -> str:
        """
        Retrieve the user's email address using the custom email authentication backend.

        Returns:
            str: The user's email address retrieved by the custom backend.
        """
        return self.backend.get_email()

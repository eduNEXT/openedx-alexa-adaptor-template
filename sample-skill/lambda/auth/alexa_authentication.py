"""Alexa Authentication Backend"""
from __future__ import annotations

from gettext import gettext as _

from ask_sdk_core.exceptions import AskSdkException
from ask_sdk_core.handler_input import HandlerInput

from auth.base_authentication import BaseEmailAuthenticationBackend


class AlexaEmailAuthentication(BaseEmailAuthenticationBackend):
    """
    Alexa Email Authentication Backend

    This authentication backend uses the User Profile Service (UPS)
    provided by Alexa to retrieve the email of the user associated

    Attributes:
        EMAIL_ERROR_MESSAGE (str): The error message displayed when
        email permissions are not granted.
    """

    EMAIL_ERROR_MESSAGE = _(
        "It was not possible to obtain the user's email. Please enable "
        "email permissions in the Alexa skill settings via the Alexa app."
    )

    def __init__(self, handler_input: HandlerInput):
        self.handler_input = handler_input

    def get_email(self) -> str | None:
        """
        Retrieve the email of the user associated with the Alexa account.

        This method attempts to fetch the user's email using the
        User Profile Service (UPS) provided by Alexa.

        Returns:
            str | None: The email of the user if successfully retrieved,
            None if the email can't be obtained.
        """
        try:
            ups_service_client = (
                self.handler_input.service_client_factory
                .get_ups_service()
            )
            return ups_service_client.get_profile_email()  # type: ignore
        except AskSdkException:
            return None

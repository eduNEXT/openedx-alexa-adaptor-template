"""Authentication Backend"""
from abc import ABC, abstractmethod
from gettext import gettext as _


class BaseEmailAuthenticationBackend(ABC):
    """
    Abstract Base Class for Authentication Backends

    This abstract class defines the interface for authentication backends in the Alexa
    skill. Subclasses must implement the `get_email` method to retrieve the email of
    the user associated with the Open edX account.

    Attributes:
        EMAIL_ERROR_MESSAGE (str): The default error message for email retrieval failure

    Methods:
        get_email: Abstract method to retrieve the user's email.
    """

    EMAIL_ERROR_MESSAGE = _("It was not possible to obtain the user's email.")

    @abstractmethod
    def get_email(self):
        """
        Abstract Method to Retrieve User Email

        This method should be implemented by subclasses to retrieve the email of the
        user associated with the Open edX account.
        """

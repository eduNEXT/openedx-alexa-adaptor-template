"""Utility functions for the Alexa skill."""
from __future__ import annotations

import os
import sys
from http import HTTPStatus
from importlib import import_module
from typing import Callable, Optional

import requests
from dotenv import load_dotenv

from constants import MAX_TIMEOUT
from auth.backends.alexa_ups import AlexaEmailAuthentication


project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(project_root, "../.."))


load_dotenv()


def make_request(
    url: str,
    method="GET",
    data: Optional[dict | str] = None,
    params: Optional[dict] = None,
    headers: Optional[dict] = None,
) -> dict:
    """
    Perform an HTTP request with the specified method.

    Args:
        url (str): The URL to send the request to.
        method (str): The HTTP method to use (e.g., "GET", "POST").
        data (dict | str, optional): The request data to include in the request body.
        headers (dict, optional): Additional headers to include in the request.
        params (dict, optional): Query parameters to include in the request URL.

    Returns:
        dict: A dictionary representing the JSON response
        if the request is successful, empty dict otherwise.
    """
    if method == "GET":
        response = requests.get(
            url, data=data, params=params, headers=headers, timeout=MAX_TIMEOUT
        )
    elif method == "POST":
        response = requests.post(url, data=data, headers=headers, timeout=MAX_TIMEOUT)
    else:
        return {}

    if response.status_code == HTTPStatus.OK:
        return response.json()

    return {}


def get_email_auth_class() -> Callable:
    """
    Get the email authentication class based on environment variables.

    This function retrieves the email authentication class to be used based
    on the value of the `SKILL_PROFILE_EMAIL_BACKEND` environment variable.
    If the variable is not set or is empty, it returns the default email
    authentication class `AlexaEmailAuthentication`.

    Returns:
        type: The class for email authentication based on the environment variable.
    """
    skill_profile_email_backend = os.getenv("SKILL_PROFILE_EMAIL_BACKEND", None)

    if not skill_profile_email_backend:
        return AlexaEmailAuthentication

    module_name, class_name = skill_profile_email_backend.rsplit(".", 1)
    module = import_module(module_name)

    return getattr(module, class_name, AlexaEmailAuthentication)

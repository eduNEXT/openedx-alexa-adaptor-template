"""Utility functions for the Alexa skill."""
from __future__ import annotations

from http import HTTPStatus
from typing import Optional

import requests

from constants import MAX_TIMEOUT


def get_request(
    url: str,
    request_data: Optional[dict] = None,
    params: Optional[dict] = None,
    headers: Optional[dict] = None,
) -> dict | None:
    """
    Perform an HTTP GET request to the specified URL.

    Args:
        url (str): The URL to send the GET request to.
        request_data (Optional[dict], optional): The request data to include
        in the request body. Defaults to None.
        params (Optional[dict], optional): Query parameters to include
        in the request URL. Defaults to None.
        headers (Optional[dict], optional): Additional headers to include
        in the request. Defaults to None.

    Returns:
        dict | None: A dictionary representing the JSON response
        if the request is successful, None otherwise.
    """
    response = requests.get(
        url, data=request_data, params=params, headers=headers, timeout=MAX_TIMEOUT
    )

    if response.status_code == HTTPStatus.OK:
        return response.json()

    return None


def post_request(
    url: str,
    request_data: dict | str,
    headers: Optional[dict] = None,
) -> dict | None:
    """
    Perform an HTTP POST request to the specified URL.

    Args:
        url (str): The URL to send the GET request to.
        request_data (Optional[dict], optional): The request data to include
        in the request body. Defaults to None.
        headers (Optional[dict], optional): Additional headers to include
        in the request. Defaults to None.

    Returns:
        dict | None: A dictionary representing the JSON response
        if the request is successful, None otherwise.
    """
    response = requests.post(
        url, data=request_data, headers=headers, timeout=MAX_TIMEOUT
    )

    if response.status_code == HTTPStatus.OK:
        return response.json()

    return None

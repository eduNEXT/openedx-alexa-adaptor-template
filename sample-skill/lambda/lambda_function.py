"""Alexa skill to get the progress of an user in a course in Open edX"""
# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
from __future__ import annotations

import gettext
import logging
from http import HTTPStatus

import ask_sdk_core.utils as ask_utils
import requests
from alexa import data
from ask_sdk_core.api_client import DefaultApiClient
from ask_sdk_core.dispatch_components import (
    AbstractExceptionHandler,
    AbstractRequestHandler,
    AbstractRequestInterceptor,
)
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_model.response import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


API_DOMAIN = "api_domain"
CLIENT_ID = "client_id"
CLIENT_SECRET = "client_secret"
GRANT_TYPE = "client_credentials"
MAX_TIMEOUT = 5


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        _ = handler_input.attributes_manager.request_attributes["_"]
        speak_output = _(data.WELCOME_MESSAGE)

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


def get_bearer_token() -> str | None:
    """Return the bearer token to consume the API

    Returns:
        str: Bearer token
        None: If the token can't be retrieved
    """
    endpoint_url = f"{API_DOMAIN}/oauth2/access_token"
    payload = (
        f"client_id={CLIENT_ID}&"
        f"client_secret={CLIENT_SECRET}&"
        f"grant_type={GRANT_TYPE}"
    )
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(
        endpoint_url, data=payload, headers=headers, timeout=MAX_TIMEOUT
    )

    if response.status_code == HTTPStatus.OK:
        return response.json()["access_token"]

    return None


def get_course_progress(username: str, course_id: str, token: str) -> float | None:
    """Return the progress of an user in a course

    Args:
        username (str): Username of the student
        course_id (str): Course id
        token (str): Bearer token to consume the API

    Returns:
        float: Progress of the student in the course
        None: If the progress can't be retrieved
    """
    endpoint_url = f"{API_DOMAIN}/eox-core/api/v1/grade/"
    payload = {"username": username, "course_id": course_id}
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(
        endpoint_url, data=payload, headers=headers, timeout=MAX_TIMEOUT
    )

    if response.status_code == HTTPStatus.OK:
        return round(response.json()["earned_grade"]*100, 2)

    return None


def get_course_id(course_name: str) -> str | None:
    """Return the course id by the course name

    Args:
        course_name (str): Course name

    Returns:
        str: Course id
        None: If the course can't be retrieved
    """
    COURSES = {
        "h5p": "course-v1:eduNEXT+H5P101+2023_T2",
        "mindmap": "course-v1:eduNEXT+MM101+2023_T2",
        "demo": "course-v1:edX+DemoX+Demo_Course",
        "limesurvey": "course-v1:edunext+lime-demo-1+2023",
        "ora": "course-v1:eduNEXT+ORA101+2023_T2",
        "openedx": "course-v1:eduNEXT+LS101+2013_T1",
    }

    return COURSES.get(course_name)


def get_profile_email(handler_input: HandlerInput) -> str | None:
    """Return the email of the user.

    Args:
        handler_input (HandlerInput): Handler input

    Returns:
        str: Email of the user
        None: If the email can't be retrieved
    """
    ups_service_client = handler_input.service_client_factory.get_ups_service()
    return ups_service_client.get_profile_email()


def get_username_by_profile_email(profile_email: str, token: str) -> str | None:
    """Return the openedx username by profile email associated to alexa account

    Args:
        profile_email (str): Email of the user
        token (str): Bearer token to consume the API

    Returns:
        str: Username of the user
        None: If the username can't be retrieved
    """
    endpoint_url = f"{API_DOMAIN}/eox-core/api/v1/user/"
    params = {"email": profile_email}
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(
        endpoint_url, params=params, headers=headers, timeout=MAX_TIMEOUT
    )

    if response.status_code == HTTPStatus.OK:
        return response.json()["username"]

    return None


def get_speak_output_get_course_progress(handler_input: HandlerInput) -> str:
    """Return the speak output for the Get Course Progress Intent

    Returns:
        str: Speak output
    """
    _ = handler_input.attributes_manager.request_attributes["_"]
    slots = handler_input.request_envelope.request.intent.slots

    profile_email = get_profile_email(handler_input)
    coursename = slots["coursename"].value.lower()

    token = get_bearer_token()

    if not token:
        return _(data.TOKEN_ERROR_MESSAGE)

    course_id = get_course_id(coursename)
    username = get_username_by_profile_email(profile_email, token)

    if not course_id:
        return _(data.COURSE_NOT_FOUND_MESSAGE)

    if not username:
        return _(data.USER_NOT_FOUND_MESSAGE)

    course_progress = get_course_progress(username, course_id, token)

    if not course_progress:
        return _(data.USER_NOT_ENROLLED_MESSAGE)

    return _(data.PROGRESS_MESSAGE).format(username, coursename, course_progress)


class GetCourseProgressIntentHandler(AbstractRequestHandler):
    """Handler for Get Course Progress in Open edX"""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_intent_name("GetCourseProgressIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:

        speak_output = get_speak_output_get_course_progress(handler_input)

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        _ = handler_input.attributes_manager.request_attributes["_"]
        speak_output = _(data.HELP_MESSAGE)
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input: HandlerInput) -> Response:
        _ = handler_input.attributes_manager.request_attributes["_"]
        speak_output = _(data.CANCEL_OR_STOP_MESSAGE)
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        _ = handler_input.attributes_manager.request_attributes["_"]
        logger.info("In FallbackIntentHandler")
        speech = _(data.FALLBACK_MESSAGE)
        reprompt = _(data.FALLBACK_REPROMPT_MESSAGE)

        return handler_input.response_builder.speak(speech).ask(reprompt).response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        # Any cleanup logic goes here.
        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive
    an error stating the request handler chain is not found, you have not implemented
    a handler for the intent being invoked or included it in the skill builder below.
    """

    def can_handle(self, handler_input: HandlerInput, exception: Exception) -> bool:
        return True

    def handle(self, handler_input: HandlerInput, exception: Exception) -> Response:
        logger.error(exception, exc_info=True)
        _ = handler_input.attributes_manager.request_attributes["_"]
        speak_output = _(data.CATCH_ALL_MESSAGE)
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class LocalizationInterceptor(AbstractRequestInterceptor):
    """Add function to request attributes, that can load locale specific data."""

    def process(self, handler_input: HandlerInput) -> None:
        """Add locale specific function to request attributes."""
        locale = handler_input.request_envelope.request.locale
        logger.info("Locale is %s", locale)

        i18n = gettext.translation(
            "data",
            localedir="locale",
            languages=[locale],
            fallback=True,
        )
        handler_input.attributes_manager.request_attributes["_"] = i18n.gettext

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = CustomSkillBuilder(api_client=DefaultApiClient())

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(GetCourseProgressIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

sb.add_global_request_interceptor(LocalizationInterceptor())

lambda_handler = sb.lambda_handler()

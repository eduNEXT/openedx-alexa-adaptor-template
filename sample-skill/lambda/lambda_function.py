"""
Alexa Skill module for Open edX

This module contains the core logic of the Alexa Skill designed to interact with the
Open edX platform. The Skill includes an example interaction that allows you to consult
the student's progress in a given course on the Open edX platform.
"""
from __future__ import annotations

import gettext
import logging
from typing import Callable

import ask_sdk_core.utils as ask_utils
from ask_sdk_core.api_client import DefaultApiClient
from ask_sdk_core.dispatch_components import (
    AbstractExceptionHandler,
    AbstractRequestHandler,
    AbstractRequestInterceptor,
)
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_model.response import Response

from alexa import data
from alexa.settings import API_DOMAIN, CLIENT_ID, CLIENT_SECRET, GRANT_TYPE
from alexa.utils import make_request, get_email_auth_class


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """
    Handler for the Skill's Launch Request.

    This handler is responsible for processing the launch request when the user
    invokes the skill. It provides a welcome message to the user.
    """

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        _ = handler_input.attributes_manager.request_attributes["_"]
        person = handler_input.request_envelope.context.system.person  # type: ignore

        if person:
            speak_output = _(data.WELCOME_MESSAGE).format(person.person_id)
            return (
                handler_input.response_builder.speak(speak_output)
                .ask(speak_output)
                .response
            )

        speak_output = _(data.PROFILE_NOT_RECOGNIZED_MESSAGE)
        return (
            handler_input.response_builder.speak(speak_output)
            .set_should_end_session(True)
            .response
        )


def get_bearer_token() -> str | None:
    """
    Retrieve the Bearer token required to consume the API.

    Returns:
        str | None: The Bearer token if successfully retrieved,
        None if the token can't be obtained.
    """
    endpoint_url = f"{API_DOMAIN}/oauth2/access_token"
    payload = (
        f"client_id={CLIENT_ID}&"
        f"client_secret={CLIENT_SECRET}&"
        f"grant_type={GRANT_TYPE}"
    )
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = make_request(endpoint_url, "POST", data=payload, headers=headers)

    return response.get("access_token")


def get_course_progress(username: str, course_id: str, token: str) -> float:
    """
    Retrieve and return the progress of a user in a specific course.

    Args:
        username (str): The username of the student.
        course_id (str): The ID of the course.
        token (str): The Bearer token used to consume the API.

    Returns:
        float: The progress of the student in the course as a percentage
        (0.00 - 100.00), or 0.0 if the progress can't be retrieved.
    """
    endpoint_url = f"{API_DOMAIN}/eox-core/api/v1/grade/"
    payload = {"username": username, "course_id": course_id}
    headers = {"Authorization": f"Bearer {token}"}

    response = make_request(endpoint_url, data=payload, headers=headers)

    return round(response.get("earned_grade", 0) * 100, 2)


def get_enrollments_by_user(username: str, token: str) -> list[str]:
    """
    Retrieve a list of course enrollments for a user. Each element of
    the list is a course ID.

    Args:
        username (str): The username of the student.
        token (str): The Bearer token used to consume the API.

    Returns:
        list[str]: A list of course IDs if enrollments are found,
        empty list if enrollments can't be retrieved.
    """
    endpoint_url = f"{API_DOMAIN}/api/enrollment/v1/enrollments/"
    params = {"username": username}
    headers = {"Authorization": f"Bearer {token}"}

    response = make_request(endpoint_url, params=params, headers=headers)

    return [result.get("course_id") for result in response.get("results", [])]


def get_courses_by_user(username: str, token: str) -> list | None:
    """
    Returns the list of all courses that a user can view.

    Args:
        username (str): The username of the student.
        token (str): The Bearer token used to consume the API.

    Returns:
        list | None: A list of courses if successfully retrieved,
        None if the courses can't be obtained.
    """
    endpoint_url = f"{API_DOMAIN}/api/courses/v1/courses/"
    params = {"username": username}
    headers = {"Authorization": f"Bearer {token}"}

    response = make_request(endpoint_url, params=params, headers=headers)

    return response.get("results")


def get_course_id(course_name: str, username: str, token: str) -> str | None:
    """
    Obtains the course ID based on the course name.

    First, it obtains the list of courses that the user can view. Then, it
    obtains the list of courses in which the user is enrolled. Finally, it
    returns the course ID if the course name is found in the list of courses.

    Args:
        course_name (str): The name of the course.
        username (str): The username of the student.
        token (str): The Bearer token used to consume the API.

    Returns:
        str | None: The course ID if found, None if the course cannot be retrieved.
    """
    enrollments = get_enrollments_by_user(username, token)
    all_courses = get_courses_by_user(username, token)

    if not enrollments or not all_courses:
        return None

    valid_courses = {}
    for course in all_courses:
        if course["id"] in enrollments:
            valid_courses[course["name"].lower()] = course["id"]

    return valid_courses.get(course_name)


def get_email(email_auth_instance: Callable) -> tuple[str | None, str | None]:
    """
    Retrieve the user's email using a flexible authentication backend.

    This function is designed to retrieve the user's email address using a
    flexible authentication backend, allowing variations based on the provided
    `email_auth_instance`. It attempts to fetch the user's email address, and if
    successful, returns it along with an error message (if any).

    Args:
        email_auth_instance (object): An instance of an authentication backend with
        a 'get_email' method.

    Returns:
        tuple[str | None, str | None]: A tuple containing two elements:
            - The error message (str) if there was an error during email retrieval,
              otherwise None.
            - The email (str) of the user if successfully retrieved, otherwise None.
    """
    error_message = None

    email = email_auth_instance.get_email()

    if not email:
        error_message = email_auth_instance.EMAIL_ERROR_MESSAGE

    return error_message, email


def get_username_by_email(email: str, token: str) -> str | None:
    """
    Retrieve the Open edX username associated with the email.

    Args:
        email (str): The email address of the user.
        token (str): The Bearer token used to consume the API.

    Returns:
        str | None: The username of the user if successfully retrieved,
        None if the username can't be obtained.
    """
    endpoint_url = f"{API_DOMAIN}/eox-core/api/v1/user/"
    params = {"email": email}
    headers = {"Authorization": f"Bearer {token}"}

    response = make_request(endpoint_url, params=params, headers=headers)

    return response.get("username")


def get_speak_output_get_course_progress(
    handler_input: HandlerInput, email_auth_instance: Callable
) -> str:
    """
    Generate the speak output for the GetCourseProgressIntent.

    This function generates the spoken response for the GetCourseProgressIntent in
    an Alexa skill. It uses the provided email authentication instance to retrieve
    the user's email address, which is then used to fetch the course progress for a
    specified course. If any errors occur during the process, appropriate error messages
    are returned in the spoken response.

    Args:
        handler_input (HandlerInput): The input handler for the request.
        email_auth_instance (Callable): A callable instance of the email
        authentication class.

    Returns:
        str: The speak output containing course progress information or error messages.
    """
    _ = handler_input.attributes_manager.request_attributes["_"]
    slots = handler_input.request_envelope.request.intent.slots  # type: ignore

    error_message, email = get_email(email_auth_instance)

    if error_message:
        return error_message

    coursename = slots["coursename"].value.lower()

    token = get_bearer_token()

    if not token:
        return _(data.TOKEN_ERROR_MESSAGE)

    username = get_username_by_email(email, token)

    if not username:
        return _(data.USER_NOT_FOUND_MESSAGE).format(email)

    course_id = get_course_id(coursename, username, token)

    if not course_id:
        return _(data.COURSE_NOT_FOUND_MESSAGE)

    course_progress = get_course_progress(username, course_id, token)

    if not course_progress:
        return _(data.USER_NOT_ENROLLED_MESSAGE)

    return _(data.PROGRESS_MESSAGE).format(username, coursename, course_progress)


class GetCourseProgressIntentHandler(AbstractRequestHandler):
    """
    Handler for the Skill's GetCourseProgressIntent

    This handler processes user requests to retrieve and provide course progress
    information from the Open edX platform.
    """

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_intent_name("GetCourseProgressIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        email_auth_class = get_email_auth_class()
        email_auth_instance = email_auth_class(handler_input)

        speak_output = get_speak_output_get_course_progress(
            handler_input, email_auth_instance
        )

        return (
            handler_input.response_builder.speak(speak_output)
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
            handler_input.response_builder.speak(speak_output)
            .ask(speak_output)
            .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_intent_name("AMAZON.CancelIntent")(
            handler_input
        ) or ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        _ = handler_input.attributes_manager.request_attributes["_"]
        speak_output = _(data.CANCEL_OR_STOP_MESSAGE)
        return handler_input.response_builder.speak(speak_output).response


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
            handler_input.response_builder.speak(speak_output)
            .ask(speak_output)
            .response
        )


class LocalizationInterceptor(AbstractRequestInterceptor):
    """
    Interceptor for handling localization in the Alexa Skill.

    This interceptor is responsible for handling the localization of the Skill.
    It retrieves the locale of the request and sets the appropriate translation
    """

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

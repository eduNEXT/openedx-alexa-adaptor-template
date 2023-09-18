"""Alexa skill to get the progress of an user in a course in Open edX"""
# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
from __future__ import annotations

import logging
from http import HTTPStatus

import ask_sdk_core.utils as ask_utils
import requests
from ask_sdk_core.api_client import DefaultApiClient
from ask_sdk_core.dispatch_components import (
    AbstractExceptionHandler,
    AbstractRequestHandler,
)
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_model.response import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)



ENDPOINT = "https://lms.valencia.athena.edunext.link"
CLIENT_ID = "client_id"
CLIENT_SECRET = "client_secret"
GRANT_TYPE = "client_credentials"
MAX_TIMEOUT = 5
OUTPUT_MESSAGES = {
    "WELCOME_MESSAGE": (
        "Bienvenido, este es el asistente de Open edX, te puedo brindar "
        "información sobre las métricas de los estudiantes y aspectos "
        "importantes de un curso."
    ),
    "JWT_ERROR_MESSAGE": "No fue posible consultar el progreso por un error de acceso.",
    "COURSE_NOT_FOUND_MESSAGE": "El curso no se encuentra. Intente con uno válido.",
    "USER_NOT_FOUND_MESSAGE": "El usuario no se encuentra. Intente con uno válido.",
    "PROGRESS_MESSAGE": (
        "El progreso para el estudiante con nombre de usuario {} "
        "en el curso de {} es {}%."
    ),
    "HELP_MESSAGE": "Hola, intenta pidiendo tu progreso en algún curso",
}


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        speak_output = OUTPUT_MESSAGES["WELCOME_MESSAGE"]

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


def get_jwt_token() -> str | None:
    """Return the jwt token to consume the API

    Returns:
        str: Bearer token
        None: If the token can't be retrieved
    """
    url = f"{ENDPOINT}/oauth2/access_token"
    payload = f'client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&grant_type={GRANT_TYPE}'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.post(url, data=payload, headers=headers, timeout=MAX_TIMEOUT)

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
    url = f"{ENDPOINT}/eox-core/api/v1/grade/"
    payload = {"username": username, "course_id": course_id}
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, data=payload, headers=headers, timeout=MAX_TIMEOUT)

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
    url = f"{ENDPOINT}/eox-core/api/v1/user/"
    params = {"email": profile_email}
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, params=params, headers=headers, timeout=MAX_TIMEOUT)

    if response.status_code == HTTPStatus.OK:
        return response.json()["username"]

    return None


def get_speak_output_get_course_progress(handler_input: HandlerInput) -> str:
    """Return the speak output for the Get Course Progress Intent

    Returns:
        str: Speak output
    """
    slots = handler_input.request_envelope.request.intent.slots

    profile_email = get_profile_email(handler_input)
    coursename = slots["coursename"].value.lower()

    token = get_bearer_token()

    if not token:
        return OUTPUT_MESSAGES["JWT_ERROR_MESSAGE"]

    course_id = get_course_id(coursename)
    username = get_username_by_profile_email(profile_email, token)

    if not course_id:
        return OUTPUT_MESSAGES["COURSE_NOT_FOUND_MESSAGE"]

    if not username:
        return "El usuario no se encuentra. Intente con uno válido."

    course_progress = get_course_progress(username, course_id, token)

    if not course_progress:
        return OUTPUT_MESSAGES["USER_NOT_FOUND_MESSAGE"]

    return OUTPUT_MESSAGES["PROGRESS_MESSAGE"].format(
        username, coursename, course_progress
    )


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
        speak_output = OUTPUT_MESSAGES["HELP_MESSAGE"]
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
        speak_output = "¡Hasta pronto!"
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
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, no estoy seguro. Puedes decir Hola o Ayuda. ¿Qué quieres hacer?"
        reprompt = "No te entendí. ¿En qué puedo ayudarte?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        # Any cleanup logic goes here.
        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """

    def can_handle(self, handler_input: HandlerInput, exception: Exception) -> bool:
        return True

    def handle(self, handler_input: HandlerInput, exception: Exception) -> Response:
        logger.error(exception, exc_info=True)
        speak_output = (
            "Lo siento, he tenido problemas para hacer lo "
            "que me pedías. Por favor, inténtalo de nuevo."
        )
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

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
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()

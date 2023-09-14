"""Alexa skill to get the progress of an user in a course in Open edX"""
# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging

import ask_sdk_core.utils as ask_utils
import requests
from ask_sdk_core.dispatch_components import (
    AbstractExceptionHandler,
    AbstractRequestHandler,
)
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_model.response import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        speak_output = (
            "Bienvenido, este es el asistente de Open edX, te puedo brindar "
            "información sobre las métricas de los estudiantes y aspectos "
            "importantes de un curso."
        )

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


COURSES = {
    "h5p": "course-v1:eduNEXT+H5P101+2023_T2",
    "mindmap": "course-v1:eduNEXT+MM101+2023_T2",
    "demo": "course-v1:edX+DemoX+Demo_Course",
    "limesurvey": "course-v1:edunext+lime-demo-1+2023",
    "ora": "course-v1:eduNEXT+ORA101+2023_T2",
    "openedx": "course-v1:eduNEXT+LS101+2013_T1",
}

# Settings
ENDPOINT = "https://lms.valencia.athena.edunext.link"
CLIENT_ID = "client_id"
CLIENT_SECRET = "client_secret"
GRANT_TYPE = "client_credentials"
MAX_TIMEOUT = 5


def get_access_token() -> tuple:
    """Return the access token to consume the API"""
    error_message, access_token = None, None

    url = f"{ENDPOINT}/oauth2/access_token"
    payload = f'client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&grant_type={GRANT_TYPE}'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.post(url, data=payload, headers=headers, timeout=MAX_TIMEOUT)

    if response.status_code == 200:
        access_token = response.json()["access_token"]
    else:
        error_message =  "No fue posible consultar el progreso por un error de acceso."

    return access_token, error_message


def get_course_progress(username: str, coursename: str) -> str:
    """Return the progress of an user in a course"""
    access_token, error_message = get_access_token()

    if not access_token:
        return error_message

    url = f"{ENDPOINT}/eox-core/api/v1/grade/"
    payload = {"username": username, "course_id": COURSES.get(coursename)}
    headers = headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, data=payload, headers=headers, timeout=MAX_TIMEOUT)

    if response.status_code == 200:
        course_progress = response.json()["earned_grade"]
        return (
            f"El progreso para el estudiante con nombre de usuario {username} "
            f"en el curso de {coursename} es {round(course_progress*100, 2)}%."
        )
    else:
        return "El usuario o el curso no se encuentra. Intente con uno válido."


class GetCourseProgressIntentHandler(AbstractRequestHandler):
    """Handler for Get Course Progress in Open edX"""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_intent_name("GetCourseProgressIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        slots = handler_input.request_envelope.request.intent.slots

        coursename = slots["coursename"].value.lower()
        username = slots["username"].value.lower()

        speak_output = get_course_progress(username, coursename)

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
        speak_output = (
            "Hola, intenta pidiendo el progreso de un estudiante en algún curso"
        )
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


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(GetCourseProgressIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()

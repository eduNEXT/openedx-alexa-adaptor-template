"""
All the strings used in the skill are defined here.

This module contains predefined messages that are used by the Open edX
assistant to provide answers to user queries.
"""

from gettext import gettext as _

WELCOME_MESSAGE = _("Welcome, this is the Open edX assistant, I can provide you information about student metrics and important aspects of a course.")
TOKEN_ERROR_MESSAGE = _("It was not possible to consult the progress due to an access error.")
COURSE_NOT_FOUND_MESSAGE = _("The course is not found. Try with a valid one.")
USER_NOT_ENROLLED_MESSAGE = _("The user is not enrolled in the course. Try with a valid one.")
USER_NOT_FOUND_MESSAGE = _("The user is not found. Try with a valid one.")
PROGRESS_MESSAGE = _("The progress for the student with username {} in the course of {} is {}%.")
HELP_MESSAGE = _("Hi, try asking for your progress in some course")
CANCEL_OR_STOP_MESSAGE = _("See you soon!")
FALLBACK_MESSAGE = _("Hmm, I'm not sure. You can say Hello or Help. What do you want to do?")
FALLBACK_REPROMPT_MESSAGE = _("I did not understand you. How can I help you?")
CATCH_ALL_MESSAGE = _("Sorry, I've had trouble doing what you asked me. Please try again.")

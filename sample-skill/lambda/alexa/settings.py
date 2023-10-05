"""Settings for the Alexa skill."""
import os

from dotenv import load_dotenv

load_dotenv()

API_DOMAIN = os.getenv("API_DOMAIN")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
GRANT_TYPE = os.getenv("GRANT_TYPE")
MAX_TIMEOUT = int(os.getenv("MAX_TIMEOUT", "5"))
SKILL_PROFILE_EMAIL_BACKEND = os.getenv("SKILL_PROFILE_EMAIL_BACKEND")

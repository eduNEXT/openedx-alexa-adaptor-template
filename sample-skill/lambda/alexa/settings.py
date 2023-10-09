"""Settings for the Alexa skill."""
import os

from dotenv import load_dotenv

load_dotenv()

LMS_DOMAIN = os.getenv("LMS_DOMAIN")
EOX_CORE_CLIENT_ID = os.getenv("EOX_CORE_CLIENT_ID")
EOX_CORE_CLIENT_SECRET = os.getenv("EOX_CORE_CLIENT_SECRET")
EOX_CORE_GRANT_TYPE = os.getenv("EOX_CORE_GRANT_TYPE")
REQUEST_MAX_TIMEOUT = int(os.getenv("REQUEST_MAX_TIMEOUT", "5"))
SKILL_PROFILE_EMAIL_BACKEND = os.getenv("SKILL_PROFILE_EMAIL_BACKEND")

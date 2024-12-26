import os
from dotenv import load_dotenv

FAKE_API_URL = "https://api-onecloud.multicloud.tivit.com/fake/"
REMOTE_TOKEN_URL = FAKE_API_URL + "token"
REMOTE_USER_URL = FAKE_API_URL + "user"
REMOTE_ADMIN_URL = FAKE_API_URL + "admin"

DATABASE_URL = "sqlite:///k2_database.db"

load_dotenv()

USER_USERNAME = os.getenv("USER_USERNAME")
USER_PASSWORD = os.getenv("USER_PASSWORD")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")


for env_variable in [USER_USERNAME, USER_PASSWORD, ADMIN_USERNAME, ADMIN_PASSWORD]:
    if not env_variable:
        raise EnvironmentError(
            f"Required environment variable ´{env_variable}´ is missing."
        )

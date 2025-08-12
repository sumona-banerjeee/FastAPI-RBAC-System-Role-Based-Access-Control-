from dotenv import load_dotenv
import os

load_dotenv()

SUPERADMIN_EMAIL = os.getenv("SUPERADMIN_EMAIL")
SUPERADMIN_PASSWORD = os.getenv("SUPERADMIN_PASSWORD")
SECRET_KEY = os.getenv("SECRET_KEY", "secret")
ALGORITHM = "HS256"
SUPERADMIN_APPROVAL_TOKEN = os.getenv("SUPERADMIN_APPROVAL_TOKEN")

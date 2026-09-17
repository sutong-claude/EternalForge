"""Shared inbox constants. Never log token values."""

from datetime import timedelta

TOKEN_ENV_PATH = "ETERNALFORGE_GOOGLE_TOKEN_PATH"
TOKEN_ENV_DIR = "ETERNALFORGE_CONFIG_DIR"
CLIENT_ID_ENV = "ETERNALFORGE_GOOGLE_CLIENT_ID"
CLIENT_SECRET_ENV = "ETERNALFORGE_GOOGLE_CLIENT_SECRET"
DEFAULT_TOKEN_NAME = "google-token.json"
GMAIL_LIST_URL = "https://gmail.googleapis.com/gmail/v1/users/me/messages"
GMAIL_GET_URL = "https://gmail.googleapis.com/gmail/v1/users/me/messages/{id}"
DRIVE_LIST_URL = "https://www.googleapis.com/drive/v3/files"
TOKEN_REFRESH_URL = "https://oauth2.googleapis.com/token"
HTTP_TIMEOUT = 8
EXPIRY_SKEW = timedelta(seconds=60)

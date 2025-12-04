"""oauth implementation."""

from authlib.integrations.starlette_client import OAuth
import os
from dotenv import load_dotenv

load_dotenv()

oauth = OAuth()

oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url=os.getenv("GOOGLE_SERVER_METADATA_URL"),
    client_kwargs={"scope": "openid email profile"},
    authorize_url=os.getenv("AUTHORIZE_URL"),
    access_token_url=os.getenv("ACCESS_TOKEN_URL"),
)

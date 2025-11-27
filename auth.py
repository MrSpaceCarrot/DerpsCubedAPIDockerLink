# Module Imports
import logging
from typing import Optional
from fastapi import HTTPException, status, Security
from fastapi.security import APIKeyHeader
from config import settings

# Logger
logger = logging.getLogger("services")

# Setup headers
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

# Authenticate against the auth key set in settings
class Authenticator:
    def __call__(self, api_key: Optional[str] = Security(api_key_header)) -> dict:

        # Validate Key
        if api_key:
            if api_key == settings.AUTH_KEY:
                return
            
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

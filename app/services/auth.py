from fastapi import Header, HTTPException, status

from app.core.config import settings


def require_api_token(authorization: str = Header(default="")) -> None:
    expected = f"Bearer {settings.api_token}"
    if authorization != expected:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

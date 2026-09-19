# auth.py
import os
from clerk_backend_api import Clerk
from clerk_backend_api.jwks import AuthenticateRequestOptions
from config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer()
clerk = Clerk(bearer_auth=settings.CLERK_SECRET_KEY)

def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    token = credentials.credentials

    try:
        request_state = clerk.authenticate_request(
            token=token,
            options=AuthenticateRequestOptions(
                jwt_key=settings.CLERK_PUBLIC_KEY,
                # Restricts tokens to ones sent by your frontend domain(s)
                authorized_parties=["http://localhost:3000", "https://your-app.com"]
            )
        )

        if not request_state.is_authenticated:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Unauthorized: {getattr(request_state, 'reason', 'Invalid token')}",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_id = request_state.payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing user ID claim",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user_id

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
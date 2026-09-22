# authClerk.py
import os
from clerk_backend_api import Clerk,AuthenticateRequestOptions
from config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Dict
from schemas import AuthUser
from userMethods import UserMethods
from database import AsyncSession,get_db
from models import UserModel
from config import settings
security = HTTPBearer()
clerk = Clerk(bearer_auth=settings.CLERK_SECRET_KEY)



def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> AuthUser:
    token = credentials.credentials

    try:
        request_state = clerk.authenticate_request(
            token=token,
            options=AuthenticateRequestOptions(
                jwt_key=settings.CLERK_PUBLIC_KEY,
                #make it be loaded from environment
                authorized_parties=settings.AUTHORIZED_PARTIES
            ),
        )

        if not request_state.is_authenticated:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Unauthorized: {getattr(request_state, 'reason', 'Invalid token')}",
                headers={"WWW-Authenticate": "Bearer"},
            )

        payload = getattr(request_state, "payload", {}) or {}
        user_id = payload.get("sub")
        email = payload.get("email")

        if not user_id or not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing user ID or email claims",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return AuthUser(clerk_user_id=user_id, email=email)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired token: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )
async def auth_user(
    db: AsyncSession = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user),
) -> UserModel:
    return await UserMethods.get_or_create_user(db,current_user)
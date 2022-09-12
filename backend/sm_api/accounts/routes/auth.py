"""
Authentication router
"""

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi_jwt_auth import AuthJWT

from sm_api.accounts.models.auth import AccessToken, RefreshToken
from sm_api.accounts.models.user import User, UserAuth
from sm_api.accounts.util.password import hash_password


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
async def login(request: Request, user_auth: UserAuth, auth: AuthJWT = Depends()):
    """Authenticates and returns the user's JWT"""
    user = await User.by_email(user_auth.email, request.state.app)
    if user is None or hash_password(user_auth.password) != user.password:
        raise HTTPException(status_code=401, detail="Bad email or password")
    access_token = auth.create_access_token(subject=user.email)
    refresh_token = auth.create_refresh_token(subject=user.email)
    return RefreshToken(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh")
async def refresh(auth: AuthJWT = Depends()):
    """Returns a new access token from a refresh token"""
    auth.jwt_refresh_token_required()
    access_token = auth.create_access_token(subject=auth.get_jwt_subject())
    refresh_token = auth.create_refresh_token(subject=auth.get_jwt_subject())
    return RefreshToken(access_token=access_token, refresh_token=refresh_token)


@router.get("/ping")
async def ping(auth: AuthJWT = Depends()):
    """Pings a protected route"""
    auth.jwt_required()
    return {"result": "success"}

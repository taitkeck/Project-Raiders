"""
Current user dependency
"""

from fastapi import Depends, HTTPException, Request
from fastapi_jwt_auth import AuthJWT

from sm_api.accounts.models.user import User


async def current_user(request: Request, auth: AuthJWT = Depends()) -> User:
    """Returns the current authorized user"""
    auth.jwt_required()
    user = await User.by_email(auth.get_jwt_subject(), request.state.app)
    if user is None:
        raise HTTPException(404, "Authorized user could not be found")
    return user


async def current_user_optional(request: Request, auth: AuthJWT = Depends()) -> User:
    """Returns the current authorized user if authenticated. Else return None."""
    try:
        auth.jwt_optional()
        user = await User.by_email(auth.get_jwt_subject(), request.state.app)
        return user
    finally:
        return None

"""
User router
"""

from fastapi import APIRouter, Depends, Response
from fastapi_jwt_auth import AuthJWT

from sm_api.accounts.models.user import User, UserOut, UserUpdate
from sm_api.accounts.util.current_user import current_user

router = APIRouter(prefix="/user", tags=["User"])


@router.get("", response_model=UserOut)
async def get_user(user: User = Depends(current_user)):
    """Returns the current user"""
    return user


@router.patch("", response_model=UserOut)
async def update_user(update: UserUpdate, user: User = Depends(current_user)):
    """Update allowed user fields"""
    user = user.copy(update=update.dict(exclude_unset=True))
    await user.save()
    return user


@router.delete("")
async def delete_user(user: User = Depends(current_user)):
    """Delete current user"""
    await user.delete()
    return Response(status_code=204)

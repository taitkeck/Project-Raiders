"""
Registration router
"""

from fastapi import APIRouter, Body, Depends, HTTPException, Request, Response
from fastapi_jwt_auth import AuthJWT
from pydantic import EmailStr

from sm_api.accounts.models.user import User, UserAuth, UserOut
from sm_api.accounts.util.mail import send_password_reset_email
from sm_api.accounts.util.password import hash_password

router = APIRouter(prefix="/register", tags=["Register"])


@router.post("", response_model=UserOut)
async def user_registration(request: Request, user_auth: UserAuth):
    """Creates a new user"""
    user = await User.by_email(user_auth.email, request.state.app)
    if user is not None:
        raise HTTPException(409, "User with that email already exists")
    hashed = hash_password(user_auth.password)
    user = User(email=user_auth.email, password=hashed, app=request.state.app)
    await user.create()
    return user


@router.post("/forgot-password")
async def forgot_password(
    request: Request, email: EmailStr = Body(..., embed=True), auth: AuthJWT = Depends()
):
    """Sends password reset email"""
    user = await User.by_email(email, request.state.app)
    if user.email_confirmed_at is not None:
        raise HTTPException(400, "Email is already verified")
    if user.disabled:
        raise HTTPException(400, "Your account is disabled")
    token = auth.create_access_token(user.email)
    await send_password_reset_email(email, token)
    return Response(status_code=200)


@router.post("/reset-password/{token}", response_model=UserOut)
async def reset_password(
    request: Request,
    token: str,
    password: str = Body(..., embed=True),
    auth: AuthJWT = Depends(),
):
    """Reset user password from token value"""
    # Manually assign the token value
    auth._token = token  # pylint: disable=protected-access
    user = await User.by_email(auth.get_jwt_subject(), request.state.app)
    if user.email_confirmed_at is not None:
        raise HTTPException(400, "Email is already verified")
    if user.disabled:
        raise HTTPException(400, "Your account is disabled")
    user.password = hash_password(password)
    await user.save()
    return user

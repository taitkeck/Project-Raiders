"""
Server app config
"""

# pylint: disable=import-error

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.middleware.sessions import SessionMiddleware
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from sm_api.apps.models.app import App
from sm_api.apps.util.default_app import get_default_app


from sm_api.config import CONFIG
from sm_api.accounts.models.user import User
from sm_api.shop.models.cart import Cart
from sm_api.shop.models.paypal import PayPalOrder
from sm_api.shop.models.product import Product
from sm_api.apps.middleware import APIKeyMiddleware


app = FastAPI(debug=True)
app.add_middleware(
    SessionMiddleware, session_cookie="fastsession", secret_key="some-random-string"
)
app.add_middleware(APIKeyMiddleware)


@app.on_event("startup")
async def app_init():
    """Initialize application services"""
    app.client = AsyncIOMotorClient(CONFIG.mongo_uri)
    # https://roman-right.github.io/beanie/tutorial/initialization/
    await init_beanie(
        app.client[CONFIG.db_name],
        document_models=[User, Product, PayPalOrder, App, Cart],
    )
    # get default app
    await get_default_app()


@AuthJWT.load_config
def get_config():
    """Load AuthJWT settings"""

    return CONFIG


@app.exception_handler(AuthJWTException)
def jwt_exception_handler(request: Request, exc: AuthJWTException):
    """Returns any authentication failures"""
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

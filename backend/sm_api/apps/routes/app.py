"""
Cart router
"""

from fastapi import APIRouter, Depends, Request, Body, Response, status
from fastapi_jwt_auth import AuthJWT
from beanie import PydanticObjectId
from sm_api.apps.models.app import App, AppBase
from sm_api.apps.util.api_key import key_gen

router = APIRouter(prefix="/app", tags=["App"])


@router.post("", response_model=App)
async def app_create(
    request: Request,
    app_data: AppBase,
    auth: AuthJWT = Depends(),
):
    """Creates a new app"""

    # auth.jwt_required()
    app = App(**app_data.dict(), api_key=key_gen())
    await app.create()
    return app


@router.get("/{id}")
async def app_get(request: Request, id: PydanticObjectId):
    """Permissions: Admin Only"""
    app = App.find_one(id=id)
    return app


@router.patch("/{id}/new_key")
async def app_gen_new_api_key(request: Request):
    """Permissions: Admin Only"""
    pass


@router.delete("/{id}")
async def app_delete(request: Request, id: PydanticObjectId):
    app = App.find_one(id=id)
    return app.remove(id)

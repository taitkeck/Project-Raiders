"""
Product router
"""

from typing import List
from fastapi import APIRouter, Depends, Response, Request
from fastapi_jwt_auth import AuthJWT
from datetime import datetime
from sm_api.apps.models.app import App

from sm_api.shop.models.product import Product, ProductBase, ProductList, ProductRead

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=ProductList)
async def list_products(request: Request, skip: int = 0, limit: int = 10):
    """Returns a list of products"""
    # https://fastapi.tiangolo.com/tutorial/query-params/#query-parameters
    product_cursor = Product.find_many(Product.app == request.state.app)
    products = await product_cursor.skip(skip).limit(limit).to_list()
    count = await product_cursor.count()
    return {"count": count, "products": products}


@router.post("", response_model=ProductRead)
async def create_product(request: Request, data: ProductBase):
    """Creates a Product"""
    product = Product(
        **data.dict(), date_modified=datetime.now(), app=request.state.app
    )
    await product.create()
    return product


# @router.delete("")
# async def delete_user(auth: AuthJWT = Depends()):
#     """Delete current user"""
#     auth.jwt_required()
#     await User.find_one(User.email == auth.get_jwt_subject()).delete()
#     return Response(status_code=204)

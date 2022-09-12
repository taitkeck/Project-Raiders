"""
Cart router
"""

from typing import Optional
from fastapi import APIRouter, Depends, Request, Body, HTTPException
from beanie import PydanticObjectId
from sm_api.shop.models.cart import Cart, CartRead, CartAddProduct
from sm_api.shop.models.product import Product, ProductBase
from sm_api.shop.util.cart import get_cart_read
from sm_api.accounts.models.user import User
from sm_api.accounts.util.current_user import current_user, current_user_optional

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.post("", status_code=201)
async def cart_add(
    request: Request,
    body: CartAddProduct = Body(...),
    user: User | None = Depends(current_user_optional),
):
    cart_db = None if body.id is None else await Cart.get(body.id)
    cart = (
        cart_db if cart_db else Cart(user=user, app=request.state.app, products=dict())
    )
    product = await Product.get(body.product_id)
    if product:
        p_dict = {**product.dict(), "quantity": body.quantity}
        cart.products[str(body.product_id)] = ProductBase(**p_dict)
    await cart.save()
    return get_cart_read(cart)


@router.get("")
async def cart_get(request: Request, user: User = Depends(current_user)):
    cart = await Cart.find_one(Cart.user == user)
    if cart is None:
        raise HTTPException(404, "No cart found for current user")
    return get_cart_read(cart)


@router.delete("/{id}")
async def cart_delete(request: Request, id: PydanticObjectId):
    cart = await Cart.get(id)
    await cart.delete()
    return {"result": "deleted"}


@router.delete("/{id}/{product_id}")
async def cart_delete_product(
    request: Request, id: PydanticObjectId, product_id: PydanticObjectId
):
    cart = await Cart.get(id)
    cart.delete_product(str(product_id))
    await cart.save()
    return get_cart_read(cart)

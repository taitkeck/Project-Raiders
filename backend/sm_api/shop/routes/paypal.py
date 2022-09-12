"""
PayPal router
"""

from fastapi import APIRouter, Depends, Response, status
from fastapi_jwt_auth import AuthJWT
from datetime import datetime

from sm_api.shop.models.paypal import PayPalOrder, PayPalOrderCreate

router = APIRouter(prefix="/paypal", tags=["PayPal"])


@router.get("/{id}", response_model=PayPalOrder | None)
async def get_paypal_order():
    """Returns a PayPal Order"""
    order = await PayPalOrder.find_one(id=id)
    return order


@router.post("", response_model=PayPalOrder, status_code=status.HTTP_201_CREATED)
async def create_paypal_order(data: PayPalOrderCreate):
    """Creates a PayPal Order"""
    data_dict = data.dict()
    paypal_id = data_dict.pop("id")
    order = PayPalOrder(**data_dict, paypal_id=paypal_id)
    await order.create()
    return order

"""
Receipt models
"""

# pylint: disable=too-few-public-methods

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Dict, Optional, List

from beanie import Document
from pydantic import BaseModel, Field, EmailStr, HttpUrl


class PayPalName(BaseModel):
    """For name validation in a PayPalOrder"""

    given_name: str
    surname: str


class PayPalPayer(BaseModel):
    name: PayPalName
    email_address: EmailStr
    payer_id: str
    address: Dict[str, str]


class PayPalPaymentSource(BaseModel):
    class PayPal(BaseModel):
        name: PayPalName
        email_address: EmailStr
        account_id: str
        address: Dict[str, str]

    paypal: PayPal


class PayPalPurchaseItem(BaseModel):
    class UnitAmount(BaseModel):
        currency_code: str = Field(max_length=3)
        value: Decimal = Field(max_digits=8, decimal_places=2)

    name: str = Field(max_length=127)
    quantity: int = Field(default=1, ge=0)
    unit_amount: UnitAmount


class PayPalPurchaseUnit(BaseModel):
    """
    See https://developer.paypal.com/docs/api/orders/v2/#definition-purchase_unit.
    """

    class PayPalAmount(BaseModel):
        class Breakdown(BaseModel):
            item_total: Dict[str, str]

        currency_code: str
        value: str
        breakdown: Optional[Breakdown]

    class PayPalPayee(BaseModel):
        email_address: EmailStr
        merchant_id: str

    class PayPalShipping(BaseModel):
        class Name(BaseModel):
            full_name: str

        name: Name
        address: Dict[str, str]

    reference_id: str = Field(default="default", max_length=256)
    amount: PayPalAmount
    payee: PayPalPayee
    shipping: PayPalShipping

    items: List[PayPalPurchaseItem]


class PayPalAPILink(BaseModel):
    """
    Links for GET, PATCH, and other actions related to the PayPal order.
    """

    class Method(str, Enum):
        """
        https://developer.paypal.com/docs/api/orders/v2/#definition-link_description.
        """

        GET = "GET"
        POST = "POST"
        PUT = "PUT"
        DELETE = "DELETE"
        HEAD = "HEAD"
        CONNECT = "CONNECT"
        OPTIONS = "OPTIONS"
        PATCH = "PATCH"

    href: HttpUrl
    rel: str = Field(description="Link Relation Type", max_length=100)
    method: Method


class PayPalOrderBase(BaseModel):
    class Intent(str, Enum):
        AUTHORIZE = "AUTHORIZE"
        CAPTURE = "CAPTURE"

    class Status(str, Enum):
        CREATED = "CREATED"
        SAVED = "SAVED"
        APPROVED = "APPROVED"
        VOIDED = "VOIDED"
        COMPLETED = "COMPLETED"
        PAYER_ACTION_REQUIRED = "PAYER_ACTION_REQUIRED"

    intent: Intent
    payment_source: PayPalPaymentSource
    status: Status
    payer: PayPalPayer
    create_time: datetime = Field(description="Create time on PayPal's system")

    purchase_units: List[PayPalPurchaseUnit]
    links: List[PayPalAPILink]


class PayPalOrderCreate(PayPalOrderBase):
    id: str = Field(max_length=50)


class PayPalOrder(Document, PayPalOrderBase):
    paypal_id: str = Field(max_length=50)

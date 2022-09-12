from typing import Dict, Optional
from decimal import Decimal
from beanie import Document
from pydantic import BaseModel, Field
from fastapi import HTTPException, status
from sm_api.apps.models.app import App
from sm_api.shop.models.product import ProductBase
from sm_api.accounts.models.user import UserOut
import iso4217parse


class Cart(Document):
    currency: str = Field(max_length=3, default="USD")
    user: Optional[UserOut]
    products: Dict[str, ProductBase]  # {id: Product}
    app: App

    def product_values(self):
        products = []
        try:
            products = [v.dict() for v in self.products.values()]
        except:
            products = [v for v in self.products.values()]
        for p in products:
            try:
                p["price"] = p["price"].to_decimal()
            except:
                pass

        return products

    def quantity(self):
        """
        Total quantity of all items in the cart.
        """
        if len(self.products) == 0:
            return 0
        return sum([v["quantity"] for v in self.product_values()])

    def price(self):
        """
        Total price of all items in the cart.
        """
        return "{:0.2f}".format(
            round(
                sum([float(v["price"]) * v["quantity"] for v in self.product_values()]),
                2,
            )
        )

    def delete_product(self, product_id: str):
        if product_id in self.products:
            del self.products[product_id]
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Product not found in cart")


class CartAddProduct(BaseModel):
    id: Optional[str]
    product_id: str
    quantity: int


class CartRead(Cart):
    """Product representation on DB get"""

    total_price: Decimal = Field(
        gte=Decimal("0.00"), decimal_places=2, max_digits=8, default=Decimal("0.00")
    )
    total_quantity: int = Field(default=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        delattr(self, "app")
        self.currency = getattr(iso4217parse.by_alpha3(self.currency), "symbols")[0]

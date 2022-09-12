"""
Product models
"""

# pylint: disable=too-few-public-methods

from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from beanie import Document
from pydantic import BaseModel, Field
from sm_api.apps.models.app import App


class ProductUpdate(BaseModel):
    """Updatable product fields"""

    quantity: Optional[int] = None
    price: Optional[Decimal] = None


class ProductBase(BaseModel):
    name: str = Field(max_length=100)
    description: str
    price: Decimal = Field(gt=Decimal("0.00"), decimal_places=2, max_digits=8)
    quantity: int = Field(default=1, ge=0)
    tags: Optional[List[str]]


class Product(Document, ProductBase):
    """Product DB representation"""

    app: App
    date_modified: datetime
    tags: List[str]

    def __repr__(self) -> str:
        return f"<Product {self.id}>"

    def __str__(self) -> str:
        return f"{self.id}: {self.name}"

    def __hash__(self) -> int:
        return hash(self.__str__())

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Product):
            return self.id == other.id
        return False

    @property
    def created(self) -> datetime:
        """Datetime Product was created from ID"""
        return self.id.generation_time


class ProductRead(Product):
    """Product representation on DB get"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        delattr(self, "app")


class ProductList(BaseModel):
    count: int
    products: List[ProductRead]

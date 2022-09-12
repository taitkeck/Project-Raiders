from enum import Enum
from typing import List
from pydantic import BaseModel, AnyHttpUrl, Field
from beanie import Document
from sm_api.apps.util.api_key import API_KEY_LEN


class Service(str, Enum):
    accounts = "accounts"
    shop = "shop"

    @classmethod
    def get_all(cls):
        return list(map(lambda s: s.value, cls))


class AppBase(BaseModel):
    name: str
    domains: List[AnyHttpUrl]
    services: List[Service]


class App(AppBase, Document):
    api_key: str = Field(max_length=API_KEY_LEN * 2, min_length=API_KEY_LEN)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, App):
            return self.id == other.id
        return False

from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

class UserCreate(BaseModel):
    email:  EmailStr
    password: str

class TokenInfo(BaseModel):
    access_token: str
    token_type: str

class UserShema(BaseModel):
    model_config = ConfigDict(strict=True)

    email: EmailStr
    password: bytes
    active: bool = True

class UserShemaAdmin(UserShema):
    is_admin: bool

class MerchItemOut(BaseModel):
    id: int
    name: str
    description: str | None
    price: int
    image_url: str | None
    quantity_available: int

    class Config:
        orm_mode = True

class MerchItemOutWithCount(MerchItemOut):
    count: int 

class PurchaseRequest(BaseModel):
    merch_item_id: int

class CoinTransfer(BaseModel):
    receiver_email: str
    amount: int

class CoinTransactionOut(BaseModel):
    type: str
    amount: int
    sender_id: int | None
    receiver_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class MerchItemCreate(BaseModel):
    name: str
    description: str | None = None
    price: int
    image_url: str | None = None
    quantity_available: int

class MerchItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: int | None = None
    image_url: str | None = None
    quantity_available: int | None = None

class UserStatsOut(BaseModel):
    email: str
    coins: int
    purchased_items: list[MerchItemOutWithCount]
    sent: list[CoinTransactionOut]
    received: list[CoinTransactionOut]


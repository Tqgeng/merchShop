from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    coins = Column(Integer, default=1000, nullable=False)
    create_at = Column(DateTime, default=datetime.utcnow)
    is_admin = Column(Boolean, default=False, nullable=False)
    active = Column(Boolean, default=True)

    purchases = relationship('Purchase', back_populates='user')

    sent_transactions = relationship('CoinTransaction', back_populates='sender', foreign_keys='CoinTransaction.sender_id')
    received_transactions = relationship('CoinTransaction', back_populates='receiver', foreign_keys='CoinTransaction.receiver_id')

class MerchItem(Base):
    __tablename__ = 'merch_items'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Integer, nullable=False)
    image_url = Column(String, nullable=True)
    quantity_available = Column(Integer, nullable=False)

    purchases = relationship('Purchase', back_populates='merch_item')

class Purchase(Base):
    __tablename__ = 'purchases'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    merch_item_id = Column(Integer, ForeignKey('merch_items.id'), nullable=False)
    purchased_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='purchases')
    merch_item = relationship('MerchItem', back_populates='purchases')

class TransactionType(enum.Enum):
    TRANSFER = 'TRANSFER'
    PURCHASE = 'PURCHASE'
    INITIAL = 'INITIAL'

class CoinTransaction(Base):
    __tablename__ = 'coin_transactions'

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    receiver_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    amount = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    type = Column(Enum(TransactionType), nullable=False)

    sender = relationship('User', back_populates='sent_transactions', foreign_keys=[sender_id])
    receiver = relationship('User', back_populates='received_transactions', foreign_keys=[receiver_id])

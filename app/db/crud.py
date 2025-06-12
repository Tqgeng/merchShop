from sqlalchemy.orm import Session
from .models import User, MerchItem, CoinTransaction, TransactionType, Purchase
from .shemas import CoinTransfer, MerchItemCreate, MerchItemUpdate, UserStatsOut, MerchItemOutWithCount
from fastapi import HTTPException, status
from collections import Counter
from passlib.hash import bcrypt

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, email: str, hashed_password: str):
    user = User(
        email = email,
        password = hashed_password,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_text_user(db: Session, hashed_password: str, email: str = None):
    db_user = db.query(User).filter(User.email == email).first()
    db_user.email = email
    db_user.password = hashed_password
    db.commit()
    db.refresh(db_user)
    return db_user

def get_merch_items(db: Session):
    return db.query(MerchItem).all()

def purchase_merch(db: Session, user: User, merch_item_id: int):
    item = db.query(MerchItem).filter(MerchItem.id == merch_item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Item not found'
        )
    if item.quantity_available < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Item is out of stock'
        )
    if user.coins < item.price:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Not coins'
        )
    
    user.coins -= item.price
    item.quantity_available -= 1

    purchase = Purchase(user_id = user.id, merch_item_id = item.id)
    transactions = CoinTransaction(
        sender_id = user.id,
        receiver_id = user.id,
        amount = -item.price,
        type = TransactionType.PURCHASE
    )

    db.add_all([purchase, transactions])
    db.commit()
    db.refresh(purchase)
    return purchase

def transfer_coins(db: Session, user: User, receiver_email: str, amount: int):
    if amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Amount not enough'
        )
    if user.coins < amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Balance not enough'
        )
    
    receiver = db.query(User).filter(User.email == receiver_email).first()
    
    if not receiver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    
    if receiver.id == user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='You cant send coins yourself'
        )
    
    user.coins -= amount
    receiver.coins += amount

    transaction = CoinTransaction(
        sender_id = user.id,
        receiver_id = receiver.id,
        amount = amount,
        type=TransactionType.TRANSFER
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction

def get_transaction_history(db: Session, user: User):
    transaction = db.query(CoinTransaction).filter(
        (CoinTransaction.sender_id == user.id) | 
        (CoinTransaction.receiver_id == user.id)
    ).order_by(CoinTransaction.created_at.desc()).all()
    return transaction


def create_merch(db: Session, merch: MerchItemCreate):
    # db_merch = MerchItem(
    #     name = merch.name,
    #     description = merch.description,
    #     price = merch.price,
    #     image_url = merch.image_url,
    #     quantity_available = merch.quantity_available
    # )
    db_merch = MerchItem(**merch.dict())
    db.add(db_merch)
    db.commit()
    db.refresh(db_merch)
    return db_merch

def update_merch(db: Session, merch: MerchItemUpdate, merch_id: int):
    db_merch = db.query(MerchItem).filter(MerchItem.id == merch_id).first()

    if not db_merch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Merch not found'
        )
    
    # db_merch.name = merch.name
    # db_merch.description = merch.description
    # db_merch.price = merch.price
    # db_merch.image_url = merch.image_url
    # db_merch.quantity_available = merch.quantity_available

    for field, value in merch.dict(exclude_unset=True).items():
        setattr(db_merch, field, value)

    db.commit()
    db.refresh(db_merch)
    return db_merch

def delete_merch(db: Session, merch_id: int):
    db_merch = db.query(MerchItem).filter(MerchItem.id == merch_id).first()

    if not db_merch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Merch not found'
        )
    
    db.delete(db_merch)
    db.commit()
    return db_merch

def get_me_info(db: Session, user: User):
    purchases = db.query(Purchase).filter(Purchase.user_id == user.id).all()

    # items = [p.merch_item for p in purchases]

    counter = Counter(p.merch_item_id for p in purchases)

    unique_items = {}
    for p in purchases:
        if p.merch_item_id not in unique_items:
            unique_items[p.merch_item_id] = p.merch_item

    purchased_items_with_count = []
    for merch_id, item in unique_items.items():
        purchased_items_with_count.append(
            MerchItemOutWithCount(**item.__dict__, count=counter[merch_id])
        )

    sent = db.query(CoinTransaction).filter(CoinTransaction.sender_id == user.id).all()
    received = db.query(CoinTransaction).filter(CoinTransaction.receiver_id == user.id).all()

    return {
        'email': user.email,
        'coins': user.coins,
        'purchased_items': purchased_items_with_count,
        'sent': sent,
        'received': received,
    }

def create_admin(db: Session):
    admin = db.query(User).filter_by(email='admin@mail.ru').first()
    if not admin:
        new_admin = User(
            email='admin@mail.ru',
            password = bcrypt.hash("admin"),
            is_admin=True
        )
        db.add(new_admin)
        db.commit()
    
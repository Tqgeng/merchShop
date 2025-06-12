from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from app.db import shemas, crud
from .auth_jwt import get_db, get_current_active_auth_user


router = APIRouter(prefix='/users', tags=['Users'])

@router.post('/transfer')
def transfer_coins(
    data: shemas.CoinTransfer,
    db: Session = Depends(get_db),
    current_user: shemas.UserShema = Depends(get_current_active_auth_user),
):
    try:
        transfer = crud.transfer_coins(db, current_user, data.receiver_email, data.amount)
        return transfer
    except HTTPException as e:
        raise e
    
@router.get('/transactions', response_model=list[shemas.CoinTransactionOut])
def get_transaction_history(
    db: Session = Depends(get_db),
    current_user: shemas.UserShema = Depends(get_current_active_auth_user)
):
    transaction = crud.get_transaction_history(db, current_user)
    return transaction

@router.get('/me', response_model=shemas.UserStatsOut)
def get_me_info(
    db: Session = Depends(get_db),
    current_user: shemas.UserShema = Depends(get_current_active_auth_user),
):
    me = crud.get_me_info(db, current_user)
    return me
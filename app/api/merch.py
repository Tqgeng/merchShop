from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from app.db import shemas, crud
from .auth_jwt import get_db, get_current_active_auth_user



router = APIRouter(prefix='/merch', tags=['Merch'])

@router.get('/', response_model=list[shemas.MerchItemOut], summary='Получить мерч')
def get_merch(db: Session = Depends(get_db)):
    return crud.get_merch_items(db)

@router.post('/purchase')
def purchase_merch(
    data: shemas.PurchaseRequest, 
    db: Session = Depends(get_db), 
    current_user: shemas.UserShema = Depends(get_current_active_auth_user),
    ):
    purchase = crud.purchase_merch(db, current_user, data.merch_item_id)
    return {'message': 'purchase successful',
            'purchase_id': purchase.id}

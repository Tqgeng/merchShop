from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from app.db import shemas, crud
from .auth_jwt import get_db, get_current_active_auth_user, get_current_admin

router = APIRouter(prefix='/admin/merch', tags=['Admins'])

@router.post('/', response_model=shemas.MerchItemOut)
def create_merch(
    merch: shemas.MerchItemCreate,
    admin = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    return crud.create_merch(db, merch)


@router.patch('/{id}', response_model=shemas.MerchItemOut)
def update_merch(
    id: int,
    merch: shemas.MerchItemUpdate,
    admin = Depends(get_current_admin), 
    db: Session = Depends(get_db)
):
    return crud.update_merch(db, merch, id)

@router.delete('/{id}')
def delete_merch(
    id: int,
    admin = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    crud.delete_merch(db, id)
    return {'message':'merch deleted'}
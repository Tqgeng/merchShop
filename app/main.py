from fastapi import FastAPI, Depends
from app.api import auth, merch, users, admin
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from app.db import crud
from app.api import auth_jwt
from sqlalchemy.orm import Session


app = FastAPI()

app.include_router(auth.router)
app.include_router(merch.router)
app.include_router(users.router)
app.include_router(admin.router)

app.mount('/frontend', StaticFiles(directory='app/frontend'))


@app.get('/', tags=['Root'], summary='Test API')
def get_root():
    return FileResponse('app/frontend/register.html')
    # return {'message': 'hello it is good'}

@app.on_event('startup')
def startup_event():
    db_generator = auth_jwt.get_db()
    db: Session = next(db_generator)
    try:
        crud.create_admin(db)
    finally:
        db.close()

if __name__ == '__main__':
    uvicorn.run('main.app', reload=True)
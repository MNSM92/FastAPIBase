from fastapi import APIRouter, Depends, status, HTTPException, Response, Request, Form, File, UploadFile
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas, models, utils, oauth2

router = APIRouter(prefix="/auth", tags=['Authentication'])



@router.get("/vpcase", response_model=schemas.ResponseSchema)
async def get_posts(db: Session = Depends(get_db),
                 current_user:int = Depends(oauth2.get_current_user)):
    if current_user:
        posts = db.query(models.VPcase).all()

        return schemas.ResponseSchema(detail="Successfully got", result={"posts": posts})
    else:
        raise


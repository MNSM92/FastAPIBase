from fastapi import APIRouter, Depends, status, HTTPException, Response, Request, Form, File, UploadFile
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas, models, utils, oauth2

router = APIRouter(prefix="", tags=['Authentication'])


@router.post('/login',
             response_model=schemas.ResponseSchema)

async def login(user_cresentials: schemas.UserLogin,
          db : Session = Depends(get_db)):

    user = db.query(models.Users).filter(models.Users.email == user_cresentials.username).first()


    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")

    user_pass_verify = utils.verify(user_cresentials.password, user.password)

    if not user_pass_verify:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return schemas.ResponseSchema(detail="Successfully login",
                                  result={"access_token": access_token, "token_type": "Bearer", "user": user} )


@router.get("/lands", response_model=schemas.ResponseSchema)
async def get_lands(db: Session = Depends(get_db),
                 current_user:int = Depends(oauth2.get_current_user)):
    if current_user:
        posts = db.query(models.LSchedule).all()

        return schemas.ResponseSchema(detail="Successfully got", result={"posts": posts})
    else:
        raise
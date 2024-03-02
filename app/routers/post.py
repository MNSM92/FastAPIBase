from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from app import models, schemas, oauth2
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
import urllib.parse

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)



@router.get("/applicationid/{id}", response_model=schemas.ResponseSchema)
async def get_application(db: Session = Depends(get_db),
              current_user: int = Depends(oauth2.get_current_user), id: str = 'f'):

    if current_user:
        posts = db.query(models.Application).filter(models.Application.id == id).first()

    else:
        raise

    return schemas.ResponseSchema(detail="Successfully got", result={"posts": posts})



@router.get("/notes/{id}", response_model=schemas.ResponseSchema)
async def get_note(id: int, db: Session = Depends(get_db),
                 current_user:int = Depends(oauth2.get_current_user)):
    if current_user:
        posts = db.query(models.Note).filter(models.Note.application_id == id).all()

        return schemas.ResponseSchema(detail="Successfully got", result={"posts": posts})
    else:
        raise


@router.get("/reports/{id}", response_model=schemas.ResponseSchema)
async def get_posts(id: int, db: Session = Depends(get_db),
                 current_user:int = Depends(oauth2.get_current_user)):
    if current_user:
        posts = db.query(models.Report).filter(models.Report.application_id == id).all()

        return schemas.ResponseSchema(detail="Successfully got", result={"posts": posts})
    else:
        raise

@router.get("/reports/", response_model=schemas.ResponseSchema)
async def get_posts(db: Session = Depends(get_db),
                 current_user:int = Depends(oauth2.get_current_user), id: str = 'f', dd: str ='f'):
    if current_user:
        posts = db.query(models.Report).filter(
            (models.Report.application_id == id) & (models.Report.report_no == dd)
        ).first()

        return schemas.ResponseSchema(detail="Successfully got", result={"posts": posts})
    else:
        raise

@router.get("/leasee", response_model=schemas.ResponseSchema)
async def get_posts(db: Session = Depends(get_db),
                 current_user:int = Depends(oauth2.get_current_user)):
    if current_user:
        posts = db.query(models.Leasee).all()

        return schemas.ResponseSchema(detail="Successfully got", result={"posts": posts})
    else:
        raise


@router.get("/lschedules/", response_model=schemas.ResponseSchema)
async def get_lschedules(db: Session = Depends(get_db),
                 current_user:int = Depends(oauth2.get_current_user), vpcase : str = 'f'):


    if current_user:

        posts = db.query(models.LSchedule).filter(models.LSchedule.vpcase == vpcase).all()

        return schemas.ResponseSchema(detail="Successfully got", result={"posts": posts})
    else:
        raise



@router.get("/leaseenid/", response_model=schemas.ResponseSchema)
async def get_lschedules(db: Session = Depends(get_db),
                 current_user:int = Depends(oauth2.get_current_user), name : str = 'f'):


    if current_user:

        posts = db.query(models.Leasee).filter(models.Leasee.name == name).all()

        return schemas.ResponseSchema(detail="Successfully got", result={"posts": posts})
    else:
        raise

@router.get("/leaseeinfo/", response_model=schemas.ResponseSchema)
async def get_lschedules(db: Session = Depends(get_db),
                 current_user:int = Depends(oauth2.get_current_user), nid : str = 'f'):


    if current_user:

        posts = db.query(models.Leasee).filter(models.Leasee.nid_number == nid).first()

        return schemas.ResponseSchema(detail="Successfully got", result={"posts": posts})
    else:
        raise


@router.get("/allapplication", response_model=schemas.ResponseSchema)
async def get_posts(db: Session = Depends(get_db),
                 current_user:int = Depends(oauth2.get_current_user)):

    if current_user:
        post = db.query(models.Application).filter(models.Application.user == current_user.role).all()

        posts = [p for p in post if p.application_status == "Active"]

        return schemas.ResponseSchema(detail="Successfully got", result={"posts": posts})
    else:
        raise



@router.get("/allapptrack", response_model=schemas.ResponseSchema)
async def get_posts(db: Session = Depends(get_db),
                 current_user:int = Depends(oauth2.get_current_user)):

    if current_user:
        post = db.query(models.Application).all()

        posts = [p for p in post if p.application_status == "Active"]

        return schemas.ResponseSchema(detail="Successfully got", result={"posts": posts})
    else:
        raise


@router.get("/approvedapplication", response_model=schemas.ResponseSchema)
async def get_posts(db: Session = Depends(get_db),
                 current_user:int = Depends(oauth2.get_current_user)):

    if current_user:
        post = db.query(models.Application).all()

        posts = [p for p in post if p.application_status == "Approved"]

        return schemas.ResponseSchema(detail="Successfully got", result={"posts": posts})
    else:
        raise

@router.get("/vpcase", response_model=schemas.ResponseSchema)
async def get_posts(db: Session = Depends(get_db),
                 current_user:int = Depends(oauth2.get_current_user)):
    if current_user:
        posts = db.query(models.VPcase).all()

        return schemas.ResponseSchema(detail="Successfully got", result={"posts": posts})
    else:
        raise


@router.get("/dcrdate/{id}", response_model=schemas.ResponseSchema)
async def get_posts(id: int, db: Session = Depends(get_db),
                 current_user:int = Depends(oauth2.get_current_user)):

    if current_user:
        posts = db.query(models.DCR).filter(models.DCR.application_id == id).first()

        return schemas.ResponseSchema(detail="Successfully got", result={"posts": posts})
    else:
        raise

@router.get("/vpcases/mouza/", response_model=schemas.ResponseSchema)
async def get_posts(db: Session = Depends(get_db),
                 current_user:int = Depends(oauth2.get_current_user), id: str ='f'):
    if current_user:
        posts = db.query(models.VPcase).filter(models.VPcase.number == id).first()

        return schemas.ResponseSchema(detail="Successfully got", result={"posts": posts})
    else:
        raise


@router.get('/alluser', response_model=schemas.ResponseSchema)

async def getusers(db: Session = Depends(get_db),
                 current_user:int = Depends(oauth2.get_current_user)):

    if current_user:
        users = db.query(models.Users.role).all()

        return schemas.ResponseSchema(detail="Successfully got",
                                  result={"posts": [user.role for user in users]} )


    else:
        raise


@router.get('/allorder/{id}', response_model=schemas.ResponseSchema)

async def getusers(id: int, db: Session = Depends(get_db),
             current_user:int = Depends(oauth2.get_current_user)):

    if current_user:
        orders = db.query(models.Note.order_no).filter(models.Note.application_id == id).all()

        return schemas.ResponseSchema(detail="Successfully got",
                                  result={"posts": [order.order_no for order in orders]} )


    else:
        raise

@router.get('/allreport/{id}', response_model=schemas.ResponseSchema)

async def getusers(id: int, db: Session = Depends(get_db),
             current_user:int = Depends(oauth2.get_current_user)):

    if current_user:
        orders = db.query(models.Report.report_no).filter(models.Report.application_id == id).all()

        return schemas.ResponseSchema(detail="Successfully got",
                                  result={"posts": [order.report_no for order in orders]} )


    else:
        raise




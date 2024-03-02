from fastapi import status, HTTPException, Depends, APIRouter
from app import models, schemas, utils, oauth2
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=['Authentication'])

@router.post("/register",
             status_code=status.HTTP_201_CREATED,
             response_model=schemas.ResponseSchema)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db),
                    get_user:int = Depends(oauth2.get_current_user)):

    #Hash
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return schemas.ResponseSchema(detail="Successfully save data!")

@router.post("/changepw",
             status_code=status.HTTP_201_CREATED,
             response_model=schemas.ResponseSchema)
def change_password(user: schemas.UpdatePW, db: Session = Depends(get_db),
                    get_user:int = Depends(oauth2.get_current_user)):

    # Get the user from the database based on the username
    if get_user:
        current_user = db.query(models.Users).filter(models.Users.username == get_user.username).first()

        hashed_new_password = utils.hash(str(user.dict()['newpassword']))

        user_pass_verify = utils.verify(user.oldpassword, current_user.password)

        if user_pass_verify:
            current_user.password = hashed_new_password
            db.commit()
            return schemas.ResponseSchema(detail="Password changed successfully")
        else:
            return schemas.ResponseSchema(detail="Old password does not match")
    else:

        raise




@router.post("/application",
             status_code=status.HTTP_201_CREATED,
             response_model=schemas.ResponseSchema)
def create_user(user: schemas.Application, db: Session = Depends(get_db),
                    get_user:int = Depends(oauth2.get_current_user)):
    if get_user:
        new_app = models.Application(**user.dict())
        db.add(new_app)
        db.commit()
        db.refresh(new_app)
        return schemas.ResponseSchema(detail="আবেদন সম্পন্ন")
    else:
        raise

@router.post("/changelands",
             status_code=status.HTTP_201_CREATED,
             response_model=schemas.ResponseSchema)
def change_user(user: schemas.LandUpdate, db: Session = Depends(get_db),
                    get_user:int = Depends(oauth2.get_current_user)):
    if get_user:
        land_change = db.query(models.LSchedule).filter(models.LSchedule.land_id == user.land_id).first()

        update_land = models.LSchedule(**user.dict())


        if land_change:
            # Delete the land_change record
            db.delete(land_change)
            db.commit()

            db.add(update_land)
            db.commit()
            db.refresh(update_land)
        else:
            db.add(update_land)
            db.commit()
            db.refresh(update_land)

        return schemas.ResponseSchema(detail="Successfully updated data!")
    else:
        raise


@router.post("/changeuser",
             status_code=status.HTTP_201_CREATED,
             response_model=schemas.ResponseSchema)
def change_user(user: schemas.SentTo, db: Session = Depends(get_db),
                    get_user:int = Depends(oauth2.get_current_user)):
    if get_user:
        user_change = db.query(models.Application).filter(models.Application.id == user.application_id).first()

        update = user.sent_to

        if user_change:
            user_change.user = update
            db.commit()
        else:
            raise

        return schemas.ResponseSchema(detail="Successfully save data!")
    else:
        raise




@router.post("/note",
             status_code=status.HTTP_201_CREATED,
             response_model=schemas.ResponseSchema)
def add_note(user: schemas.Note, db: Session = Depends(get_db),
                    get_user:int = Depends(oauth2.get_current_user)):
    if get_user:

        new_note = models.Note(**user.dict())
        update_sent_from = db.query(models.Users).filter(models.Users.role == new_note.sent_from).first()
        update_sent_to = db.query(models.Users).filter(models.Users.role == new_note.sent_to).first()
        new_note.sent_from = update_sent_from.username
        new_note.sent_to = update_sent_to.username

        db.add(new_note)
        db.commit()
        db.refresh(new_note)

        new_note = models.Note(**user.dict())
        update = new_note.sent_to
        post_query = db.query(models.Application).filter(models.Application.id == user.application_id).first()
        if post_query:
            post_query.user = update
            db.commit()
        else:
            print("No matching history record found for application ID:", user.application_id)

        return schemas.ResponseSchema(detail="Successfully save data!")
    else:
        return

@router.post("/report",
             status_code=status.HTTP_201_CREATED,
             response_model=schemas.ResponseSchema)
def add_note(user: schemas.Report, db: Session = Depends(get_db),
                    get_user:int = Depends(oauth2.get_current_user)):

    if get_user:
        new_note = models.Report(**user.dict())
        update_sent_from = db.query(models.Users).filter(models.Users.role == new_note.sent_from).first()
        update_sent_to = db.query(models.Users).filter(models.Users.role == new_note.sent_to).first()
        new_note.sent_from = update_sent_from.username
        new_note.sent_to = update_sent_to.username

        db.add(new_note)
        db.commit()
        db.refresh(new_note)

        new_note = models.Report(**user.dict())
        update = new_note.sent_to
        post_query = db.query(models.Application).filter(models.Application.id == user.application_id).first()
        if post_query:
            post_query.user = update
            db.commit()
        else:
            print("No matching history record found for application ID:", user.application_id)

        return schemas.ResponseSchema(detail="Successfully save data!")
    else:
        raise



@router.post("/dcr",
             status_code=status.HTTP_201_CREATED,
             response_model=schemas.ResponseSchema)
def add_note(user: schemas.Dcr, db: Session = Depends(get_db),
                    get_user:int = Depends(oauth2.get_current_user)):

    if get_user:

        new_note = models.DCR(**user.dict())
        signature_update = db.query(models.Users).filter(models.Users.role == "acland_sonatola").order_by(models.Users.id.desc()).first()
        new_note.signature_by = signature_update.username
        db.add(new_note)
        db.commit()
        db.refresh(new_note)

        update = "Approved"
        post_query = db.query(models.Application).filter(models.Application.id == user.application_id).first()

        renew_lands = post_query.application_for
        lands_list = list(map(str, renew_lands[:-1].split(",")))

        renew_year = post_query.applied_for

        if post_query:
            post_query.application_status = update
            db.commit()
        else:
            print("No matching history record found for application ID:", user.application_id)



        print(renew_year, lands_list)

        for i in range(len(lands_list)):
            lands_query = db.query(models.LSchedule).filter(models.LSchedule.id == lands_list[i]).first()
            print(lands_query.renewed_upto)
            if lands_query:
                lands_query.renewed_upto = int(renew_year)
                db.commit()

        return schemas.ResponseSchema(detail="Successfully save data!")
    else:
        raise




@router.post("/addleasee",
             status_code=status.HTTP_201_CREATED,
             response_model=schemas.ResponseSchema)
async def create_user(user: schemas.AddLeasee, db: Session = Depends(get_db),
                    get_user:int = Depends(oauth2.get_current_user)):
    if get_user:

        new_user = models.Leasee(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return schemas.ResponseSchema(detail="Successfully save data!")
    else:
        raise

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import schemas, models, database
from encrypter import Encrypter
from typing import List
# from License.environment import Config
from License.security import JBEncrypter, JBHash
from localDatabase import LocalDatabase
from License.security import JBEncrypter


def get_settings(key):
    value = LocalDatabase().get_settings(key)
    return JBEncrypter().decrypt(value)

router = APIRouter(
    prefix='/user',
    tags=['Users']
)
get_db = database.get_db


def is_authenticated(pp):
    # p = JBHash().hash_message_with_nonce(Config().config('ENCRYPT_PASSWORD'))
    p = JBHash().hash_message_with_nonce(get_settings('ENCRYPT_PASSWORD'))
    if pp is None or pp != p[1]:
        return False

    return True

@router.post("", response_model=schemas.UserDataResponseModel, status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.UserDataModel, db: Session = Depends(get_db), pp: str = None):
    if is_authenticated(pp) is False:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Not Authorized")

    user = db.query(models.UserModel).filter(models.UserModel.email == request.email)

    if not user.first():
        hashPwd = Encrypter().hash(request.password)
        new_user = models.UserModel(name=request.name, email=request.email, password=hashPwd)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    else:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Email Already exist in the database!")


@router.get("/all", status_code=status.HTTP_200_OK, response_model=List[schemas.UserDataResponseModel])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.UserModel).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Database is empty!")
    return users


@router.get("/{email}", status_code=status.HTTP_200_OK, response_model=schemas.UserDataResponseModel)
def get_user(email: str, db: Session = Depends(get_db)):
    user = db.query(models.UserModel).filter(models.UserModel.email == email)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with  email {email} not Found!")
    return user.first()


@router.get("/", status_code=status.HTTP_200_OK, response_model=schemas.UserDataResponseModel)
def get_user_auto(email: str ="", id: int = 0, db: Session = Depends(get_db)):
    # get user with email specified
    if email != "":
        user = db.query(models.UserModel).filter(models.UserModel.email == email)
        if not user.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with  email {email} not Found!")
        return user.first()

    # get user with id specify
    if id != 0:
        user = db.query(models.UserModel).filter(models.UserModel.id == id)
        if not user.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with  id {id} not Found!")
        return user.first()

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"no parameter")


@router.delete("/{email}", status_code=status.HTTP_200_OK)
def delete_user(email: str, db: Session = Depends(get_db), pp: str = None):
    if is_authenticated(pp) is False:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Not Authorized")

    user = db.query(models.UserModel).filter(models.UserModel.email == email)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email {email} no longer exists.!")

    user.delete(synchronize_session=False)
    db.commit()
    return {'detail': f"User with email {email} was deleted successfully"}


@router.put("/{email}", status_code=status.HTTP_200_OK)
def update_user(email: str, request: schemas.UserDataModel, db : Session = Depends(get_db), pp: str = None):
    if is_authenticated(pp) is False:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Not Authorized")

    user = db.query(models.UserModel).filter(models.UserModel.email == email)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email {email} not Found!")
    user.update({'name':request.name, 'password':request.password})
    db.commit()
    return {'detail': "Updated Successfully"}

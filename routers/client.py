from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import schemas, models, database
# from License.environment import Config
from License.security import JBEncrypter, JBHash
from localDatabase import LocalDatabase
from License.security import JBEncrypter
import os


# def get_settings(key):
#     value = LocalDatabase().get_settings(key)
#     return JBEncrypter().decrypt(value)

router = APIRouter(
    prefix="/client",
    tags=["Clients"]
)
get_db = database.get_db


def is_authenticated(pp):
    # p = JBHash().hash_message_with_nonce(Config().config('ENCRYPT_PASSWORD'))
    # p = JBHash().hash_message_with_nonce(get_settings('ENCRYPT_PASSWORD'))
    p = JBHash().hash_message_with_nonce(os.environ.get('ENCRYPT_PASSWORD'))
    if pp is None or pp != p[1]:
        return False

    return True


@router.post("", status_code=status.HTTP_201_CREATED)
def create_client(request: schemas.ClientDataModel, db: Session = Depends(get_db), pp: str = None):
    if is_authenticated(pp) is False:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Not Authorized")

    client = db.query(models.ClientModel).filter(models.ClientModel.systemId == request.systemId)
    if not client.first():
        new_client = models.ClientModel(systemId=request.systemId,
                                        systemKey = request.systemKey,
                                        trialLicenseKey = request.trialLicenseKey,
                                        fullLicenseKey = request.fullLicenseKey,
                                        trialExpired = request.trialExpired,
                                        trialActivated = request.trialActivated,
                                        messageSentSuccessfully = request.messageSentSuccessfully,
                                        active=request.active,
                                        owner_id = request.owner_id
                                        )
        db.add(new_client)
        db.commit()
        db.refresh(new_client)
        return new_client

    raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Duplicate System Id")


@router.get("/{systemId}", status_code=status.HTTP_200_OK)
def get_client(systemId: str, db: Session = Depends(get_db)):
    print("sure im here")
    client = db.query(models.ClientModel).filter(models.ClientModel.systemId == systemId)
    if not client.first():
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Client with system Id {systemId} not Found!")
        # return {'status_code': status.HTTP_404_NOT_FOUND, 'detail': f"Client with id {systemId} not Found!"}

    return client.first()


@router.get("", status_code=status.HTTP_200_OK)
def get_all_clients(db: Session = Depends(get_db)):
    clients = db.query(models.ClientModel).all()
    if not clients:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Empty Database")

    return clients



@router.delete("/{systemId}")
def delete_client(systemId: str, db: Session = Depends(get_db), pp: str = None):
    if is_authenticated(pp) is False:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Not Authorized")

    client = db.query(models.ClientModel).filter(models.ClientModel.systemId == systemId)
    if not client.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Client with email {systemId} not Found!")

    client.delete(synchronize_session=False)
    db.commit()
    data = {'status_code': status.HTTP_200_OK,
            'deleted': True,
            'detail': f"User with SystemId {systemId} deleted successfully!"}
    # print(data)
    return data


@router.put("/update/{systemId}", status_code=status.HTTP_200_OK)
def client_update(systemId: str, request: schemas.ClientDataModel, db: Session = Depends(get_db), pp: str = None):
    print('Updating client..................')
    if is_authenticated(pp) is False:
        print("not Authorized")
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Not Authorized")

    client = db.query(models.ClientModel).filter(models.ClientModel.systemId == systemId)
    if not client.first():
        print('system id not found.')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with system Id {systemId} not Found!")
    print()
    print(request)
    print()
    client.update({'systemId': request.systemId,
                    'systemKey': request.systemKey,
                    'trialLicenseKey': request.trialLicenseKey,
                    'fullLicenseKey': request.fullLicenseKey,
                    'trialExpired': request.trialExpired,
                    'trialActivated': request.trialActivated,
                    'active': request.active,
                    'messageSentSuccessfully': request.messageSentSuccessfully,
                   'owner_id': request.owner_id})

    db.commit()
    # db.refresh(client)

    return {'detail': f"client with system Id {systemId} updated successfully!"}


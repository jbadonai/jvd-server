from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import schemas, models, database
from License.licenseGen import LicenseGen
# from License.environment import Config
from License.security import JBEncrypter, JBHash
from localDatabase import LocalDatabase
from License.security import JBEncrypter
import os

#   Pyinstaller -w -y main.spec
# def get_settings(key):
#     value = LocalDatabase().get_settings(key)
#     return JBEncrypter().decrypt(value)


license_generator = LicenseGen()

router = APIRouter(
    prefix="/license",
    tags=["License"]
)

def is_authenticated(pp):
    # p = JBHash().hash_message_with_nonce(Config().config('ENCRYPT_PASSWORD'))
    # p = JBHash().hash_message_with_nonce(get_settings('ENCRYPT_PASSWORD'))
    p = JBHash().hash_message_with_nonce(os.environ.get('ENCRYPT_PASSWORD'))

    if pp is None or pp != p[1]:
        return False

    return True


# GENERATE LICENSE AND SEND VIA MAIL
@router.get("/", status_code=status.HTTP_200_OK)
async def generate_license_and_send_via_mail(systemId: str = "", systemKey: str = "", email: str = "", pp: str = None):
    if is_authenticated(pp) is False:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Not Authorized")

    if systemId != "" and systemKey != "" and email != "":
        user_license = await license_generator.generate_license(system_id=systemId, system_key=systemKey, email=email)
        email_status = await license_generator.send_license_by_email(email=email, license=user_license)
        return {'status_code': status.HTTP_200_OK, 'detail': email_status, 'user_license': user_license}
    else:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No Sufficient Data")


# CHANGE TRIAL DAYS
@router.get("/trial_days")
def change_trial_days(days: str = 3, pp: str = None):
    if is_authenticated(pp) is False:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Not Authorized")

    # Config().trial_days = days
    encDays = JBEncrypter().encrypt(days)
    LocalDatabase().update_setting('FREE_TRIAL_DAYS', encDays)

    return {'status_code': status.HTTP_200_OK, 'details':"Trial days updated!"}


#   ROUTE FOR FULL ACTIVATION
@router.get("/full_activation")
async def generate_full_license_and_send_via_mail(pp: str = None, email: str = "", payment_info: str = ""):

    if is_authenticated(pp) is False:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Not Authorized")

    if email == "" or payment_info == "":
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No Sufficient Data")

    # Generate full license
    user_license = await license_generator.generate_full_license(email=email, payment_info=payment_info)

    # send the full license to user's email address
    email_status = await license_generator.send_full_license_by_email(email=email, license=user_license)

    # update payment info for the user on the server


    # return data to the caller of the api
    return {'status_code': status.HTTP_200_OK, 'detail': email_status, 'user_license': user_license}


@router.get("/full_activation_only")
async def generate_full_license_only(pp: str = None, email: str = "", payment_info: str = ""):

    if is_authenticated(pp) is False:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Not Authorized")

    if email == "" or payment_info == "":
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No Sufficient Data")

    # Generate full license
    user_license = await license_generator.generate_full_license(email=email, payment_info=payment_info)

    # return data to the caller of the api
    return {'status_code': status.HTTP_200_OK, 'user_license': user_license}


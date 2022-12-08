from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import schemas, models, database
from License.licenseGen import LicenseGen
from License.environment import Config
from License.security import JBEncrypter, JBHash


license_generator = LicenseGen()

router = APIRouter(
    prefix="/license",
    tags=["License"]
)

def is_authenticated(pp):
    p = JBHash().hash_message_with_nonce(Config().config('ENCRYPT_PASSWORD'))
    # p = str(p).replace("=","%3D")
    print(p)
    if pp is None or pp != p[1]:
        return False

    return True


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


@router.get("/trial_days")
def change_trial_days(days: str = 3, pp: str = None):
    if is_authenticated(pp) is False:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Not Authorized")

    Config().trial_days = days

    return {'status_code': status.HTTP_200_OK, 'details':"Trial days updated!"}

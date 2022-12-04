from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import schemas, models, database
from License.licenseGen import LicenseGen

license_generator = LicenseGen()

router = APIRouter(
    prefix="/license",
    tags=["License"]
)


@router.get("/", status_code=status.HTTP_200_OK)
async def generate_license_and_send_via_mail(systemId: str = "", systemKey: str = "", email: str = ""):
    if systemId != "" and systemKey != "" and email != "":
        user_license = await license_generator.generate_license(system_id=systemId, system_key=systemKey, email=email)
        email_status = await license_generator.send_license_by_email(email=email, license=user_license)
        return {'status_code': status.HTTP_200_OK, 'detail': email_status, 'user_license': user_license}
    else:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No Sufficient Data")

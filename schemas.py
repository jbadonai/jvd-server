from pydantic import BaseModel
from typing import List


class UserDataModel(BaseModel):
    name: str
    email: str
    password: str
    payment_info: str


class ClientDataModelBase(BaseModel):
    systemId: str
    systemKey: str
    trialLicenseKey: str
    fullLicenseKey: str
    trialExpired: bool = False
    trialActivated: bool = False
    active: bool = False
    messageSentSuccessfully: bool = False
    owner_id: int


class ClientDataModel(ClientDataModelBase):
    class Config():
        orm_mode = True


class UserDataResponseModel(BaseModel):
    name: str
    email: str
    payment_info: str
    id: int
    clients: List[ClientDataModel] = []

    class Config():
        orm_mode = True


class UserDataResponseModelAuth(BaseModel):
    email: str
    password: str

    class Config():
        orm_mode = True



class ClientDataResponseModel(BaseModel):
    systemId: str
    systemKey: str
    trialLicenseKey: str
    fullLicenseKey: str
    trialExpired: bool
    trialActivated: bool
    active: bool
    messageSentSuccessfully: bool
    owner_id: int
    owner: UserDataResponseModel



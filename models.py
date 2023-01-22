from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, index=True, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    payment_info = Column(String)
    clients = relationship("ClientModel", back_populates="owner")


class ClientModel(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    systemId = Column(String)
    systemKey = Column(String)
    trialLicenseKey = Column(String)
    fullLicenseKey = Column(String)
    trialExpired = Column(Boolean)
    trialActivated = Column(Boolean)
    active = Column(Boolean)
    messageSentSuccessfully = Column(Boolean)
    owner_id = Column(Integer, ForeignKey(UserModel.id))
    owner = relationship("UserModel", back_populates="clients")



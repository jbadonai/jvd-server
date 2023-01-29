from passlib.context import CryptContext
from passlib.handlers.bcrypt import bcrypt


class Encrypter():
    def __init__(self):
        self.pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated='auto')

    def hash(self, message):
        return self.pwd_cxt.hash(message)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_cxt.verify(plain_password, hashed_password)

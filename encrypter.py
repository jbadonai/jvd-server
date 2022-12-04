from passlib.context import CryptContext


class Encrypter():
    def __init__(self):
        self.pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated='auto')

    def hash(self, message):
        return self.pwd_cxt.hash(message)

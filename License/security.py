from cryptography.fernet import Fernet
import hashlib
from urllib.request import urlopen
from datetime import timedelta
from License.environment import *
import pyrebase
import  os
import datetime
from localDatabase import LocalDatabase
from exceptionsList import *
import  platform

emergency = b'gAAAAABjzTTq_UIJXKGU5rjxgS6X6oZERFlZDCwxd1wUDuIvakyZt9dRNBIHMzHtb7h-9tcIffJdpUbQLEjn8oSkEp_18LiNlb31zx068Bm_0Wv0LJTNSl4='

def clear_screen():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def get_settings(key):
    value = LocalDatabase().get_settings(key)
    if value is None:
        return value

    return JBEncrypter().decrypt(value)



def get_config():
    try:
        fbDec = eval(JBEncrypter().decrypt(fb_config))
        fbAuth = eval(JBEncrypter().decrypt(fb_data_auth))
        print(fbDec)
        print(fbAuth)

        firebase = pyrebase.initialize_app(fbDec)

        db = firebase.database()
        auth = firebase.auth()

        def authenticate(username, password):
            try:
                result = auth.sign_in_with_email_and_password(username, password)
                idToken = result['idToken']
                return idToken
            except Exception as e:
                if str(e).__contains__("Errno 11001") or str(e).__contains__("Max retries exceeded"):
                    raise InternetConnectionException
                else:
                    return None

        def get_config():
            un = input("Username: ")
            pw = input("Password: ")

            clear_screen()

            if JBEncrypter().encrypt(un).decode() != "gAAAAABjlK9QuT2mwWNdBthmEt7mxyTklthWV-txemS0T29gH7a9FKOEzoLMFucN_ZH5DFaz8dKkO3iDCOfEYHEQYhkR4-Qnpw==":
                token = authenticate(un.strip(), pw.strip())
                if token is None:
                    raise UnAuthorizedException

            configurations = db.child("Config").get(token=token)
            config = dict(configurations.val())
            return config

        return get_config(), None
    except InternetConnectionException:
        return None, "Internet Connection issue"
    except UnAuthorizedException:
        return None, "Unauthorized user!"
    except Exception as e:
        print(f"following error occurred: {e}")
        return None, e
        pass


class JBEncrypter():

    def generate_key_from_password(self, password_provided):
        try:
            import base64
            import os
            from cryptography.hazmat.backends import default_backend
            from cryptography.hazmat.primitives import hashes
            from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

            # password_provided = "password"  # This is input in the form of a string
            password = password_provided.encode()  # Convert to type bytes
            # salt = os.urandom(16)  # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes

            salt = "jbadonaiventures".encode()  # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
            # salt = Config().config("SALT").encode()  # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
            # salt = config["SALT"].encode()  # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
            # print(f'salt = {salt}')

            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
                backend=default_backend()
            )

            key = base64.urlsafe_b64encode(kdf.derive(password))  # Can only use kdf once

            return key
        except Exception as e:
            print(f"Error Occurred in 'generate_key_from_password' : {e}")

    def encrypt(self, message, password="password"):
        # print(f"ENCRYPT PASSWORD USED IS: {password}")
        key = self.generate_key_from_password(password)
        fernet = Fernet(key)
        encMessage = fernet.encrypt(message.encode())

        return encMessage

    def decrypt(self, encMessage, password="password"):
        try:
            key = self.generate_key_from_password(password)
            fernet = Fernet(key)
            decMessage = fernet.decrypt(encMessage).decode()

            return decMessage
        except:
            return None
            pass


class JBHash():

    def hash_message_with_nonce(self, message, master_pass=None):

        password = get_settings('HASH_PASSWORD')
        if password is None:
            password = JBEncrypter().decrypt(emergency, master_pass)

        for x in range(100000000000):
            encoded_message = message.encode()
            nonce = str(x)
            # result = hashlib.sha256(encoded_message + nonce.encode() + Config().config('HASH_PASSWORD').encode())
            # result = hashlib.sha256(encoded_message + nonce.encode() + get_settings('HASH_PASSWORD').encode())
            result = hashlib.sha256(encoded_message + nonce.encode() + password.encode())


            #
            # result = hashlib.sha256(encoded_message + nonce.encode() + os.environ.get('HASH_PASSWORD').encode())
            # result = hashlib.sha256(encoded_message + nonce.encode() + config['HASH_PASSWORD'].encode())
            # print(result.hexdigest())
            if str(result.hexdigest())[:2] == "aa":
                return nonce, result.hexdigest()

        return 0

    def hashMessageWithNonce(self,application_name, message, my_nonce = None):
        if my_nonce is None:
            for x in range(100000000000):
                    message = f"{application_name}_{message}"
                    encoded_message = message.encode()
                    nonce = str(x)
                    # result = hashlib.sha256(encoded_message + nonce.encode() + Config().config('HASH_PASSWORD').encode())
                    # result = hashlib.sha256(encoded_message + nonce.encode() + get_settings('HASH_PASSWORD').encode())
                    result = hashlib.sha256(encoded_message + nonce.encode() + os.environ.get('HASH_PASSWORD').encode())
                    # result = hashlib.sha256(encoded_message + nonce.encode() + config['HASH_PASSWORD'].encode())
                    # print(result.hexdigest())
                    if str(result.hexdigest())[:3] == "afc":
                        return nonce, result.hexdigest()
            return 0

        else:
            print('here', my_nonce)
            message = f"{application_name}_{message}"
            encoded_message = message.encode()
            nonce = str(my_nonce)
            # result = hashlib.sha256(encoded_message + nonce.encode() + get_settings('HASH_PASSWORD').encode())
            result = hashlib.sha256(encoded_message + nonce.encode() + os.environ.get('HASH_PASSWORD').encode())
            # result = hashlib.sha256(encoded_message + nonce.encode() + Config().config('HASH_PASSWORD').encode())
            # result = hashlib.sha256(encoded_message + nonce.encode() + config['HASH_PASSWORD'].encode())
            # print(result.hexdigest())
            # if str(result.hexdigest())[:3] == "afc":
            return nonce, result.hexdigest()

    def hash_message(self, message):
        encoded_message = message.encode()

        result = hashlib.sha256(encoded_message)

        return result.hexdigest()

    def hash_file(self, filename):
        with open(filename, "rb") as f:
            bytes = f.read()
            hash = hashlib.sha256(bytes).hexdigest();
            return  hash


class LicenseGenerator():
    # from jbEncrypter import JBHash, JBEncrypter
    def __init__(self):
        self.encrypter = JBEncrypter()

    def get_time_online(self):
        try:
            res = urlopen('http://just-the-time.appspot.com/')
            result = res.read().strip()

            result_str = result.decode('utf-8')
            return result_str
        except Exception as e:
            pass

    def generate_license(self, minutes=None, hours=None, days=None):

        # current_time = self.get_time_online() # get time online incase local time has been tampered with.
        current_time = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))  # get time locally

        if minutes is not None:
            expire = datetime.datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S') + timedelta(minutes=minutes)

        if hours is not None:
            expire = datetime.datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S') + timedelta(hours=hours)

        if days is not None:
            expire = datetime.datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S') + timedelta(days=days)

        # return self.encrypter.encrypt(str(expire), get_settings('LICENCE_PASSWORD')).decode()
        return self.encrypter.encrypt(str(expire), os.environ.get('LICENCE_PASSWORD')).decode()
        # return self.encrypter.encrypt(str(expire), Config().config('LICENCE_PASSWORD')).decode()
        # return self.encrypter.encrypt(str(expire), config['LICENCE_PASSWORD']).decode()

    def is_license_expired(self, license):
        try:
            # expirestr = self.encrypter.decrypt(license.encode(), get_settings('LICENCE_PASSWORD'))
            expirestr = self.encrypter.decrypt(license.encode(), os.environ.get('LICENCE_PASSWORD'))
            # expirestr = self.encrypter.decrypt(license.encode(), Config().config('LICENCE_PASSWORD'))
            # expirestr = self.encrypter.decrypt(license.encode(), config['LICENCE_PASSWORD'])
            # current_time = self.get_time_online()
            current_time = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

            expire = datetime.datetime.strptime(expirestr, '%Y-%m-%d %H:%M:%S')
            now = datetime.datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
            # print('number of days:')

            days_remaining = expire - now
            # print(days_remaining)

            if now > expire:
                return True, days_remaining
            else:
                return False, days_remaining
        except:
            return True, "Invalid License!"
            pass



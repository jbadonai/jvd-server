import platform
from License.security import JBHash, JBEncrypter
import os
from exceptionsList import *
import pyrebase


class ServerSetUP():
    def __init__(self):
        self.master_pass = "aaa37d9373edbf40d3b2dff299e610f7145f7d49f2c050d12cb1561e30077ebb"
        self.master_pass_from_user = None
        self.firebase_username = None
        self.firebase_password = None
        self.authenticated = False
        self.fb_config = b'gAAAAABjx-Q4LjGhctJ16RWsOrL8mcKWLp_dynjkJWXMjppsHNi4MjhsCc-L6JnqMwpjysfDeWM7mZHKKdb8v82-uS5z5r2m3ZwJpASjHsxB51o7hGOa3tguD8E47wdgnrFTpQyDYho7jZRYK87oirTDEsJON0cmMI4ja05tSL2ai_nHJkcn_p6M4fMtK9Y5waBWtN6SXDjF0ELRpI5Cw_8pSf544W97MeE-NSDVPwaLn4iCVpVglpzVp2DXe6dYtaGzMIIcvzciAQS2MObKMlykvpUc3QN77TjWUiEdkeUeLp2K9ZS9suxKre1kAqSD-cWhNWIzKPvppz1foyar53_TtPvUaihrN-t19uSo6-iBnZKDKuqTyRFr03IOGtd0MoeVQ5NN4Ulsk162kF8rT3NyIhrJW-6JWqNFcSKtZp4EknQllCPr0Q4mtFsEV1n0H56GfvdYx2rlQHp7GRSKgkauPu1IiHPij0UiiEdzKZrz5CqaoeG7zPvWIm_kXsczhlPlud3nkesAlHRmP0ToBhkXKHTH-K1TV9gFnWN19bx4amvkPzixAVnnPYSJCS-VnX0o3DRwqccduDCqeDcI2kuVDPdeQMSadw=='
        self.fb_data_auth = b'gAAAAABjx-Q5S17UL-f-EqX3NDpLuEQ4lXT-n42ViwdUjwM7y3iCeXPO1LcR90kpdMpqIayPu4rqt7TdIAnG1aMDNeFKyVE9qozLgtMZPLvsbNsaXAJP7kAFmxiipyfqIFV3yrvBm73ub8i8lq7OVAt6T280EUpZ9Q=='
        self.config_data = None

    def clear_screen(self):
        if platform.system() == "Windows":
            os.system('cls')
        else:
            os.system('clear')

    def authenticate(self):
        try:
            master_pass = input("Pass Code: ")
            self.master_pass_from_user = master_pass
            self.clear_screen()

            check_pass = JBHash().hash_message_with_nonce(master_pass, master_pass=master_pass)[1]

            if check_pass != self.master_pass:
                raise AuthenticationException

            return True
        except AuthenticationException:
            print("Authentication Failed!")
            return False
        except Exception as e:
            print(f"An Error Occurred in authenticate; {e}")
            return False

    def get_config(self):
        try:
            # decrypt firebase coded access data to access firebase
            fbDec = eval(JBEncrypter().decrypt(self.fb_config, self.master_pass_from_user))
            fbAuth = eval(JBEncrypter().decrypt(self.fb_data_auth, self.master_pass_from_user))

            # connect to firebase to get secret data stored
            firebase = pyrebase.initialize_app(fbDec)

            # connection to firebase database
            db = firebase.database()

            # connection to firebase authentication
            auth = firebase.auth()

            def authenticate(username, password):
                # fire base authentication to get token
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
                # retrieve configuration/secret data stored in firebase. firebase login and password will be required.
                un = input("Username: ")
                pw = input("Password: ")

                self.clear_screen()

                token = authenticate(un.strip(), pw.strip())
                if token is None:
                    raise UnAuthorizedException

                # GET CONFIGURATION DATA
                configurations = db.child("Config").get(token=token)
                config = dict(configurations.val())
                self.config_data = config
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

    def set_environment_variables(self, key, value):
        try:
            os.environ[key] = str(value)
        except Exception as e:
            print(f"An Error Occurred in set environment variales: {e}")

    def intialize_setup(self):
        try:
            #   1. Authenticate
            print("[1/3] Authenticating...")
            authenticate_result = self.authenticate()
            if authenticate_result is False:
                raise AuthenticationException

            #   2. load environment data from FB
            print("[2/3] Connecting to Firebase to load configuration data...")
            data = self.get_config()[0]
            if data is None:
                raise AuthenticationException

            #   3. apply environment data on this machine
            print("[3/3] Applying configuration data")
            for d in self.config_data:
                # print(f"{d}>>{self.config_data[d]}")
                self.set_environment_variables(d, self.config_data[d])

        except AuthenticationException:
            print("Authentication issue in initial setup")
        except Exception as e:
            print(f"An Error Occurred in initialize setup: {e}")

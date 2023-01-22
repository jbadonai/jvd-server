from License.security import LicenseGenerator, JBEncrypter
# from License.environment import Config
from License.emailSender import EmailSender
import License.messageTemplates as msgTemp
from localDatabase import LocalDatabase
from License.security import JBEncrypter, JBHash
import os
import datetime


# def get_settings(key):
#     value = LocalDatabase().get_settings(key)
#     dec = JBEncrypter().decrypt(value)
#     return dec


class LicenseGen():
    def __init__(self):
        self.email_sender = EmailSender()
        pass

    async def generate_license(self, system_id, system_key, email):
        # trialLicense = LicenseGenerator().generate_license(days=int(Config().config('FREE_TRIAL_DAYS')))
        ans = LocalDatabase().is_setting_key_in_database('FREE_TRIAL_DAYS')
        print(f"Setting sin database? {ans}")
        # days = int(get_settings('FREE_TRIAL_DAYS'))
        days = int(os.environ.get('FREE_TRIAL_DAYS'))
        print(f"No of trial days: {days}")
        if days is None:
            days = 3

        trialLicense = LicenseGenerator().generate_license(days=days)
        salt = f"Trial'{email}'{system_id}'{system_key}'{trialLicense}"
        # user_license = JBEncrypter().encrypt(salt, Config().config("ENCRYPT_PASSWORD"))
        # user_license = JBEncrypter().encrypt(salt, get_settings("ENCRYPT_PASSWORD"))
        user_license = JBEncrypter().encrypt(salt, os.environ.get("ENCRYPT_PASSWORD"))

        return user_license

    async def generate_full_license(self,  email, payment_info):
        # trialLicense = LicenseGenerator().generate_license(days=int(Config().config('FREE_TRIAL_DAYS')))
        systemInfo = eval(payment_info)
        payment_gateway = systemInfo['payment_gateway']
        payment_id = systemInfo['payment_id']
        payee_id = systemInfo['payee_id']
        token = systemInfo['token']
        approved = systemInfo['approved']

        # creating license contents. license identity
        license_element = f"{email}'{payment_gateway}'{payment_id}'{payee_id}'{token}'{approved}"

        # encrypting the license content to form actual license
        main_license = JBHash().hash_message_with_nonce(license_element[1])

        salt = f"Full'{main_license}'{datetime.datetime.now()}"

        full_user_license = JBEncrypter().encrypt(salt, os.environ.get("ENCRYPT_PASSWORD"))

        return full_user_license

    async def send_license_by_email(self, email, license):
        try:
            messageHtml = await msgTemp.get_license_request_message(email, license.decode())
            # messageplain = msgTemp.get_license_request_message_plain(email, license.decode())

            days = int(os.environ.get("FREE_TRIAL_DAYS"))
            if days > 1:
                message = f"{days} days"
            else:
                message = f"{days} day"

            print(f"Message formulated::::>> {message}")
            result = await self.email_sender.send_email(From="Admin@jbadonaiventures.com",
                                                  To=email,
                                                  subject=f"{message} Free Trial License Code for JVD",
                                                  body=messageHtml)

            print(f"Email send result::::: { result}")
            return result

        except Exception as e:
            pass

    async def send_full_license_by_email(self, email, license):
        try:
            messageHtml = await msgTemp.get_full_license_request_message(email, license.decode())

            result = await self.email_sender.send_email(From="Admin@jbadonaiventures.com",
                                                  To=email,
                                                  subject=f"[JVD] - FULL LICENSE DETAILS",
                                                  body=messageHtml)

            print(f"Email send result::::: { result}")
            return result

        except Exception as e:
            pass

    async def send_paypal_payment_creation_email(self,user, email, paymentId, payerId, token):
        try:
            messageHtml = await msgTemp.get_paypal_payment_created_message(email, paymentId, payerId, token)

            result = await self.email_sender.send_email(From="Admin@jbadonaiventures.com",
                                                  To=email,
                                                  subject=f"[JVD]-PAYMENT CREATED SUCCESSFULLY FOR '{user}'",
                                                  body=messageHtml)

            print(f"Email send result::::: { result}")
            return result

        except Exception as e:
            pass


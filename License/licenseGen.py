from License.security import LicenseGenerator, JBEncrypter
from License.environment import Config
from License.emailSender import EmailSender
import License.messageTemplates as msgTemp


class LicenseGen():
    def __init__(self):
        self.email_sender = EmailSender()
        pass

    async def generate_license(self, system_id, system_key, email):
        trialLicense = LicenseGenerator().generate_license(days=int(Config().config('FREE_TRIAL_DAYS')))
        salt = f"Trial'{email}'{system_id}'{system_key}'{trialLicense}"
        user_license = JBEncrypter().encrypt(salt, Config().config("ENCRYPT_PASSWORD"))

        return user_license

    async def send_license_by_email(self, email, license):
        try:
            messageHtml = await msgTemp.get_license_request_message(email, license.decode())
            # messageplain = msgTemp.get_license_request_message_plain(email, license.decode())


            days = int(Config().config("FREE_TRIAL_DAYS"))
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


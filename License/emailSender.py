from email.message import EmailMessage
import smtplib
import ssl
import os
# from License.environment import Config as config
# from main import myConfig
from localDatabase import LocalDatabase
from License.security import JBEncrypter


# def get_settings(key):
#     value = LocalDatabase().get_settings(key)
#     return JBEncrypter().decrypt(value)


class EmailSender():
    def __init__(self):
        self.em = None
        pass

    async def send_email(self, From, To, subject, body):
        try:
            self.em = EmailMessage()
            self.em['From'] = From
            self.em['To'] = To
            self.em['Subject'] = subject
            self.em.set_content(body, subtype='html')

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                # smtp.login(Config().config('EMAIL_ADDRESS'), Config().config('EMAIL_PASSWORD'))
                # smtp.login(get_settings('EMAIL_ADDRESS'), get_settings('EMAIL_PASSWORD'))
                smtp.login(os.environ.get('EMAIL_ADDRESS'), os.environ.get('EMAIL_PASSWORD'))
                smtp.send_message(msg=self.em, from_addr=From, to_addrs=To)
            print("Email Sent successfully")
            return {'status': "Success", 'detail':"Email Sent Successfully"}
        except Exception as e:
            if '[Errno 11001]' in str(e) or '10054':
                print("Internet Connection issue. Please check your internet connection")
                return {'status': "Failed", 'detail': "Internet Connection issue. Please check your internet connection"}
            else:
                print(f"An Error occurred in sendEmail(): {e}")
                return {'status': "Failed", 'detail': f"The following Error Occurred: {e}"}

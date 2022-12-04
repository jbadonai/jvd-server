from email.message import EmailMessage
import smtplib
import ssl
from License.environment import Config


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
                smtp.login(Config().config('EMAIL_ADDRESS'), Config().config('EMAIL_PASSWORD'))
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

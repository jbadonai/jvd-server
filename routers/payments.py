from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import schemas, models, database
from encrypter import Encrypter
from typing import List
# from License.environment import Config
from License.security import JBEncrypter, JBHash
from localDatabase import LocalDatabase
from License.security import JBEncrypter
from payments import paypal
import os
from payments.paypal import PaypalPayment
from License.licenseGen import LicenseGen

license_generator = LicenseGen()

router = APIRouter(
    prefix='/payments',
    tags=['Payments']
)

get_db = database.get_db



def is_authenticated(pp):
    # p = JBHash().hash_message_with_nonce(Config().config('ENCRYPT_PASSWORD'))
    # p = JBHash().hash_message_with_nonce(get_settings('ENCRYPT_PASSWORD'))
    p = JBHash().hash_message_with_nonce(os.environ.get('ENCRYPT_PASSWORD'))
    if pp is None or pp != p[1]:
        return False

    return True


def process_payment(payment_gateway):
    try:
        if payment_gateway == 'paypal':
            create_paypal_payment()
    except Exception as e:
        print(f"An Error Occurred in process payment: {e}")


async def start_paypal_payment_creation(user_data=None):
    try:
        data = None
        paypal_payment = PaypalPayment()
        await paypal_payment.configure_payement()
        await paypal_payment.set_payment_details(amount=float(os.environ['PAID_LICENSE_AMOUNT']), other_data=user_data)
        await paypal_payment.create_payment()

        data = {'payment_object': paypal_payment.payment, 'approval_url': paypal_payment.approval_url}

        return data

    except Exception as e:
        print(f"An Error Occurred in process paypal payment: {e}")


async def start_paypal_payment_execution(paymentId, payeeId, token):
    try:
        paypal_payment = PaypalPayment()
        result = await paypal_payment.execute_payment(paymentId, payeeId)

        return result
    except Exception as e:
        print(f"An error occurred in payments > start paypal payment execution: {e}")


# CREATE PAYMENT FOR PAYPAL
@router.get("/paypal")
async def create_payment_for_paypal(user_data=None):
    try:
        # CREATE PAYMENT
        # to return 'approval url' and 'payment object' as data to the client
        # approval url will be open for client user to make payment
        data = await start_paypal_payment_creation(user_data=user_data)

        return {'status_code': status.HTTP_200_OK, 'detail': data}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No Sufficient Data")


#   EXECUTE THE PAYMENT
#   this is requested and executed after user has finished paying and has received payment id, payee id and token
@router.get("/paypal/execute")
async def create_payment_for_paypal(paymentId=None,payeeId=None, token=None, user_data=None):
    try:
        if paymentId is None or payeeId is None or token is None or user_data is None:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No Sufficient Data")

        data = await start_paypal_payment_execution(paymentId, payeeId, token)
        if data['error_details'] is None:
            # No Error. Payment approved. send details to user via mail
            userData = eval(user_data)
            email = userData['email']
            username = userData['username']

            #   TRY TO SEND PAYEMENT DATA TO USER
            print("Sending Email....")
            email_status = await license_generator.send_paypal_payment_creation_email(user=username, email=email, paymentId=paymentId,
                                                                                       payerId=payeeId, token=token)
            print("Email Sent!")
            print(f"Email Status: {email_status}")
        return {'status_code': status.HTTP_200_OK, 'detail': data}
    except Exception as e:
        return str(e)

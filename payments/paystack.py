import os
from PyQt5 import QtCore
import time
import requests
import json
import logging as paystack_logging
import datetime

class PaymentError(Exception):
    pass


class PaystackPayment():
    def __init__(self):
        self.amount = os.environ.get('PAID_LICENSE_AMOUNT_NAIRA')
        self.transaction = None
        self.transaction_manager = None
        self._initialize_paystack()


    def _initialize_paystack(self):
        PaystackConfig.SECRET_KEY = os.environ.get('PAYSTACK_TEST_SECRET_KEY')
        PaystackConfig.PUBLIC_KEY = os.environ.get('PAYSTACK_TEST_PUBLIC_KEY')
        self.transaction_manager = TransactionsManager()

    async def create_paystack_transaction(self, customer_email):

        transactionAmount = int(self.amount) * 100
        transaction = Transaction(transactionAmount, customer_email)
        # transaction_manager = TransactionsManager()
        self.transaction = self.transaction_manager.initialize_transaction('STANDARD', transaction)

        # return the whole transaction object and authorization url
        return self.transaction

    def verify_Transaction(self, transaction):
            try:
                ans = self.transaction_manager.verify_transaction(transaction)
            except Exception as e:
                time.sleep(1)


class VerifyThread(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(dict)

    def __init__(self, transaction_manager, transaction):
        super(VerifyThread, self).__init__()
        self.transactionManager = transaction_manager
        self.transaction = transaction
        self.emitData = {}

    def stop(self):
        self.requestInterruption()

    def run(self):
        try:
            counter = 0
            while True:
                counter += 1
                self.emitData['info'] = f"\rwaiting[{counter}]..."
                self.any_signal.emit(self.emitData)
                try:
                    ans = self.transactionManager.verify_transaction(self.transaction)
                    self.emitData['data'] = ans
                    self.any_signal.emit(self.emitData)
                    break
                except:
                    time.sleep(1)
                    continue

        except Exception as e:
            pass


class JbaPaystackPayments():
    def __init__(self):
        self.amount = float(os.environ.get('PAID_LICENSE_AMOUNT_NAIRA')) * 100

        go_live = bool(int(os.environ.get('GO_LIVE')))
        if go_live is True:
            self.secret_key = os.environ.get('PAYSTACK_LIVE_SECRET_KEY')
        else:
            self.secret_key = os.environ.get('PAYSTACK_TEST_SECRET_KEY')

        paystack_logging.basicConfig(filename='paystack_transactions.log', level=paystack_logging.INFO)


    def initialize_payment(self, token=None, email="none@none.com"):
        # Set the API endpoint
        url = "https://api.paystack.co/transaction/initialize"

        # Set the headers
        headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json"
        }

        # Set the request data
        data = {
            "amount": self.amount,  # Replace with your desired amount
            "email": email,  # Replace with the customer's email address
            # "callback_url": f"https://jbadonai.github.io/jbadonaiventures-webpage/thankyou.html?appToken={token}",  # Replace with your callback URL
            "callback_url": f"{os.environ.get('PAYPAL_RETURN_URL')}?appToken={token}",  # Replace with your callback URL
            "metadata": {
                "custom_fields": [
                    {
                        "display_name": "Mobile Number",
                        "variable_name": "mobile_number",
                        "value": "+2348000000000"  # Replace with the customer's mobile number
                    }
                ]
            }
        }

        try:
            # Send the request
            response = requests.post(url, headers=headers, data=json.dumps(data))

            # Parse the response
            if response.status_code == 200:
                response_data = response.json()
                authorization_url = response_data["data"]["authorization_url"]
                access_code = response_data["data"]["access_code"]
                reference = response_data["data"]["reference"]
                paystack_logging.info(f"[Payment Created Successfully] - owner: {email}, amount: {self.amount}, reference:{reference}"
                                  f"access_code: {access_code}, url:{authorization_url}, "
                                  f"date:{datetime.datetime.today()}")
                return authorization_url, access_code, reference
            else:
                paystack_logging.info(
                    f"[Payment Creation Failed] - owner: {email}, amount: {self.amount}, "
                    f"date:{datetime.datetime.today()}, error_details:{response.status_code}: {response.text}")
                raise PaymentError(f"Error {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            paystack_logging.info(
                f"[Payment Creation Failed] - owner: {email}, amount: {self.amount}, "
                f"date:{datetime.datetime.today()}, error_details:Error connecting to payment gateway: {str(e)}")
            raise PaymentError(f"Error connecting to payment gateway: {str(e)}")

    async def verify_payment(self, reference):
        # Set the API endpoint
        url = f"https://api.paystack.co/transaction/verify/{reference}"

        # Set the headers
        headers = {
            "Authorization": f"Bearer {self.secret_key}"
        }

        try:
            # Send the request
            response = requests.get(url, headers=headers)

            # Parse the response
            if response.status_code == 200:
                response_data = response.json()
                status = response_data["data"]["status"]
                amount = response_data["data"]["amount"]
                currency = response_data["data"]["currency"]
                transaction_date = response_data["data"]["transaction_date"]
                error_details = None
                paystack_logging.info(f"[TRANSACTION COMPLETED]: status: {status}, reference:{reference},"
                                  f"amount: {amount}, currency: {currency}, transaction_date: {transaction_date}")
                return status, amount, currency, transaction_date, error_details
            else:
                error_details = f"Error {response.status_code}: {response.text}"
                paystack_logging.info(f"[TRANSACTION ERROR]: reference{reference}, error_details:  {response.status_code}: {response.text}")
                return None, None, None, None, error_details

        except requests.exceptions.RequestException as e:
            error_details = f"Error connecting to payment gateway: {str(e)}"
            paystack_logging.info(f"[TRANSACTION ERROR]: reference{reference}, error_details: Error connecting to payment gateway: {str(e)} ")
            return None, None, None, None, error_details


'''
paystack verified result sample:

{
  "status": true,
  "message": "Verification successful",
  "data": {
    "id": 2546369282,
    "domain": "test",
    "status": "success",
    "reference": "frvjxeck7u",
    "amount": 2000,
    "message": null,
    "gateway_response": "Successful",
    "paid_at": "2023-02-18T07:50:45.000Z",
    "created_at": "2023-02-18T07:50:13.000Z",
    "channel": "card",
    "currency": "NGN",
    "ip_address": "41.190.31.105",
    "metadata": "",
    "log": {
      "start_time": 1676706639,
      "time_spent": 7,
      "attempts": 1,
      "errors": 0,
      "success": true,
      "mobile": false,
      "input": [],
      "history": [
        {
          "type": "action",
          "message": "Attempted to pay with card",
          "time": 6
        },
        {
          "type": "success",
          "message": "Successfully paid with card",
          "time": 7
        }
      ]
    },
    "fees": 30,
    "fees_split": null,
    "authorization": {
      "authorization_code": "AUTH_a8er4n99f2",
      "bin": "408408",
      "last4": "4081",
      "exp_month": "12",
      "exp_year": "2030",
      "channel": "card",
      "card_type": "visa ",
      "bank": "TEST BANK",
      "country_code": "NG",
      "brand": "visa",
      "reusable": true,
      "signature": "SIG_sV4NbMS92tEjhlxbVIcx",
      "account_name": null
    },
    "customer": {
      "id": 112536355,
      "first_name": null,
      "last_name": null,
      "email": "jba@yahoo.com",
      "customer_code": "CUS_bhdfkaaxigv89e7",
      "phone": null,
      "metadata": null,
      "risk_action": "default",
      "international_format_phone": null
    },
    "plan": null,
    "split": {},
    "order_id": null,
    "paidAt": "2023-02-18T07:50:45.000Z",
    "createdAt": "2023-02-18T07:50:13.000Z",
    "requested_amount": 2000,
    "pos_transaction_data": null,
    "source": null,
    "fees_breakdown": null,
    "transaction_date": "2023-02-18T07:50:13.000Z",
    "plan_object": {},
    "subaccount": {}
  }
}

'''
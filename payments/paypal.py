import paypalrestsdk
import logging
import webbrowser
import sqlite3
import os


class PaypalPayment():
    def __init__(self):
        self.payment = None
        self.browser = None
        self.approval_url = None

        self.initialize()

    def initialize(self):
        try:
            logging.basicConfig(filename='transactions.log', level=logging.INFO)
        except Exception as e:
            print(f"An Error Occurred in initialize: {e}")

    def open_url(self, url):
        try:
            # Get the default browser
            self.browser = webbrowser.get()
            webbrowser.open(url=url)

        except Exception as e:
            print(f"An Error Occurred in open url: {e}")

    async def configure_payement(self):
        try:
            # Configure the SDK with your API credentials
            paypalrestsdk.configure({
                "mode": "sandbox", # or "live"
                "client_id": os.environ.get('PAYPAL_CLIENT_ID'),
                "client_secret": os.environ.get('PAYPAL_CLIENT_SECRET')
            })
        except Exception as e:
            print(f"An Error Occurred in configure payment. {e}")

    async def set_payment_details(self, other_data=None, amount=7.00, description="JVD License"):
        try:
            token = None
            if other_data is not None:
                other_data = eval(other_data)

            token = other_data['token']

            # Create a payment
            amount = float(os.environ.get('PAID_LICENSE_AMOUNT'))
            self.payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal"
                },
                "redirect_urls": {
                    # "return_url": "https://jbadonai.github.io/jbadonaiventures-webpage/thankyou.html",
                    # "cancel_url": "https://jbadonai.github.io/jbadonaiventures-webpage/cancel.html"
                    "return_url": f"{os.environ.get('PAYPAL_RETURN_URL')}?token={token}",
                    "cancel_url": os.environ.get('PAYPAL_CANCEL_URL'),

                },
                "transactions": [{
                    "amount": {
                        "total": amount,
                        "currency": "USD"
                    },
                    "description": description
                }]
            })
        except Exception as e:
            print(f"An Error Occurred in set payment details: {e}")

    async def create_payment(self):
        try:
            # Create the payment
            if self.payment.create():
                print("Payment created!")
                # Get the payment approval URL
                approval_url = None
                for link in self.payment.links:
                    if link.method == "REDIRECT":
                        approval_url = link.href
                        # open_url(approval_url)
                        self.approval_url = approval_url
                        break

                if approval_url:
                    print("Redirect user to approval_url")
                else:
                    print("Error: Approval URL not found")
            else:
                print("Error creating payment:", self.payment.error)
        except Exception as e:
            print(f"An Error Occurred in create payment: {e}")

    async def execute_payment(self, payment_id, payer_id):
        # Get payment ID and payer ID from the user
        # payment_id = input("Enter the payment ID: ")
        # payer_id = input("Enter the payer ID: ")

        # Execute the payment
        try:
            payment = paypalrestsdk.Payment.find(payment_id)
        except Exception as e:
            data = {'status': 'Payment Execution Failed', 'error_details': str(e)}
            return data

        if payment.execute({"payer_id": payer_id}):
            if payment.state == "approved":
                # log status
                logging.info("Transaction succeeded: Payment ID: %s, Payer ID: %s, Amount: %s %s", payment.id, payer_id,
                             payment.transactions[0].amount.total, payment.transactions[0].amount.currency)
                print("Payment approved!")
                data = {'status': 'Payment Approved!', 'error_details': None}
                return data
            else:
                logging.error("Transaction failed: Payment ID: %s, Payer ID: %s, Error: %s", payment.id, payer_id,
                              payment.error)
                print("Error executing payment:", payment.error)
                print("Payment not approved!")
                data = {'status': 'Payment Not Approved!', 'error_details': payment.error}
                return data
        else:
            print("Error executing payment:", payment.error)
            data = {'status': 'Payment Not Approved!', 'error_details': payment.error}
            return data




    # def start_payment():
    #     configure_payement()
    #     set_payment_details()
    #     create_payment()
    #     execute_payment()


def log_to_local_database():

    # Connect to the database
    conn = sqlite3.connect('transactions.db')

    # Create the transactions table if it doesn't exist
    conn.execute('''CREATE TABLE IF NOT EXISTS transactions
                    (id INTEGER PRIMARY KEY,
                    payment_id TEXT,
                    payer_id TEXT,
                    amount REAL,
                    currency TEXT,
                    status TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP);''')

    # ...

    if payment.execute({"payer_id": payer_id}):
        # Log the transaction details to the database
        conn.execute("INSERT INTO transactions (payment_id, payer_id, amount, currency, status) VALUES (?, ?, ?, ?, ?)",
                     (payment.id, payer_id, payment.transactions[0].amount.total,
                      payment.transactions[0].amount.currency, payment.status))
        conn.commit()
        print("Payment executed successfully!")
    else:
        # Log the error
        conn.execute("INSERT INTO transactions (payment_id, payer_id, status, error_message) VALUES (?, ?, ?, ?)",
                     (payment.id, payer_id, "failed", payment.error))
        conn.commit()
        print("Error executing payment:", payment.error)

    # Close the connection
    conn.close()

def log_to_loggly():
    import logging
    from loggly.handlers import HTTPSHandler

    #pip install loggly-python-handler

    # Configure the loggly handler
    loggly_handler = HTTPSHandler(
        'your-customer-token', 'logs-01.loggly.com', use_json=True
    )

    # Configure the logger
    logger = logging.getLogger('loggly')
    logger.setLevel(logging.INFO)
    logger.addHandler(loggly_handler)

    # ...

    if payment.execute({"payer_id": payer_id}):
        # Log the transaction details
        logger.info({'payment_id': payment.id, 'payer_id': payer_id, 'amount': payment.transactions[0].amount.total,
                     'currency': payment.transactions[0].amount.currency, 'status': payment.status})
        print("Payment executed successfully!")
    else:
        # Log the error
        logger.error({'payment_id': payment.id, 'payer_id': payer_id, 'error': payment.error})
        print("Error executing payment:", payment.error)
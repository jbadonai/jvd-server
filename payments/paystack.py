from python_paystack.paystack_config import PaystackConfig
import  time
PaystackConfig.SECRET_KEY  = "sk_test_5c8a0783ae14b5ebf4729c987bfb91b65435bd2d"
PaystackConfig.PUBLIC_KEY = "pk_test_39d1f87f9b682fe96c54d10a53134b0497f8913d"

from python_paystack.objects.transactions import Transaction
from python_paystack.managers import TransactionsManager

transaction = Transaction(5000, 'jayadonai@yahoo.com')
transaction_manager = TransactionsManager()
transaction = transaction_manager.initialize_transaction('STANDARD', transaction)
#Starts a standard transaction and returns a transaction object

print(transaction.authorization_url)
#Gives the authorization_url for the transaction
# input('wait')
counter = 0
while True:
    counter += 1
    print(f"\rwaiting[{counter}]...", end="")
    try:
        ans = transaction_manager.verify_transaction(transaction)
        break
    except:
        continue
    time.sleep(1)

#Transactions can easily be verified like so
# ans = transaction_manager.verify_transaction(transaction)

print("metadata: ", ans.metadata)
print("email: ", ans.email)
print("auth code: ", ans.authorization_code)
print("ref code: ", ans.generate_reference_code())
print("card locale: ", ans.card_locale)
print("plan: ", ans.plan)
print("reference: ", ans.reference)
print("trans charge: ", ans.transaction_charge)
print("trans charge: ", ans.transaction_charge)

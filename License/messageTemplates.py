import os
import datetime

# from License.environment import Config
from localDatabase import LocalDatabase
from License.security import JBEncrypter

#
# def get_settings(key):
#     value = LocalDatabase().get_settings(key)
#     return JBEncrypter().decrypt(value)


async def get_license_request_message(user, license_key):
    # days = int(Config().config("FREE_TRIAL_DAYS"))
    # days = int(get_settings("FREE_TRIAL_DAYS"))
    days = int(os.environ.get("FREE_TRIAL_DAYS"))
    if days > 1:
        message = f"{days} days"
    else:
        message = f"{days} day"

    License_request_message =f"""<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
Dear {str(user).split("@")[0]},<br>
<p>
    Thank you for downloading JBA Video Downloader!<br><br>
    Below is your {message} Free Trial Licence code:
</p>
<p><b>Licence key: </b></p>
<div style="border:2px dashed gray; padding:10px;color:blue;">    
    {license_key}
</div>

<div>
    <p>To apply Your Free Licence:</p>
    <li>
        <ol>
            <li>Copy the license Code above.</li>
            <li>Go back to JBA Video Downloader.</li>
            <li>Open the settings menu by clicking on the gear icon on the tool bar. (<i>if it's not opened already</i>)</li>
            <li>Paste your licence code in the space provided.</li>
            <li>Click on 'Activate License' button.</li>
        </ol>
    </li>
    <p>You are good to go!</p>
</div>

</body>
</html>

"""

    return License_request_message


async def get_full_license_request_message(user, license_key):

    License_request_message =f"""<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
Dear {str(user).split("@")[0]},<br>
<p>
    Thank you for purchasing JBA Video Downloader!<br><br>
    Below is your Full Licence code:
</p>
<p><b>Licence key: </b></p>
<div style="border:2px dashed gray; padding:10px;color:blue;">    
    {license_key}
</div>

<div>
<p>We will try to automatically apply your license to your copy of JVD. But if this fails, you can do it manually by following the steps below:</p>
    <br><p>To apply Your FULL Licence manually:</p>
    <li>
        <ol>
            <li>Copy the license Code above.</li>
            <li>Go back to JBA Video Downloader.</li>
            <li>Open the settings menu by clicking on the gear icon on the tool bar. (<i>if it's not opened already</i>)</li>
            <li>Paste your licence code in the space provided.</li>
            <li>Click on 'Activate License' button.</li>
        </ol>
    </li>
    <p>You are good to go!</p>
</div>

</body>
</html>

"""

    return License_request_message


async def get_paypal_payment_created_message_bak(email, paymentId, payerId, token):

    head = """
    <head>
  <title>Thank You For Your Payment</title>
  <style>
    /* Responsive Styles */
    @media only screen and (max-width: 600px) {
      .container {
        width: 90%;
        margin: 0 auto;
      }
      .card {
        width: 80%;
        margin: 0 auto;
      }
    }

/* General Styles */
body {
  background-color: rgb(45,45,45);
color: rgb(0,225,127);
}

      /* position and style logo */
      .logo {
        position: fixed;
        top: 10px;
        left: 10px;
        width: 70px;
        height: 70px;
        z-index: 1;

	padding: auto;

	margin: auto;
      }
      .left-aligned-div {
        text-align: left;
      }
	.page-center{
	margin: 50px auto;
	color: yellow;
}

.container {
  width: 80%;
  margin: 0 auto;
}
      .card {
        width: 70%;
        height: Auto;
        margin: 50px auto;
        background: rgb(220,220,220);
	color:black;
        box-shadow: 0px 0px 10px #000000;
        border-radius: 10px;
        text-align: center;
        padding: 20px;
      }
h1{
  text-align: center;
  margin-top: 30px;
}

span {
position: relative; /* Add this */
  word-wrap: break-word;
  white-space: pre-wrap;
  overflow-wrap: break-word;

}

.info {
  text-align: center;
  margin: 50px auto;

}

.key{
color: blue;
margin:5px;
padding: 5px;

}
.fa-copy:before {
    content: "\f0c5";
    font-family: "Font Awesome 5 Free";
}
.fa-copy {
    font-size: 20px; /* adjust the size of the icon */
    color: blue; /* adjust the color of the icon */
    cursor: pointer; /* change cursor to pointer on hover */
     position: absolute; /* This is already there */
    top: 0;
    right: 0;
}


footer {
  width: 100%;
  text-align: center;
  margin-top: 50px;
  padding: 20px;
}
  </style>
</head>
    """

    payment_created_message =f"""<html lang="en">
{head}
<body>
Dear {str(email).split("@")[0]},<br>

<div class="container">
    <h1>Thank you for your payment!</h1>
    <p class="info">Your transaction has been completed successfully.</p>

    <div class="card">
        <p><b>PAYMENT ID:</b> <strong><span class="key" id="paymentId-value">{paymentId}</span></strong></p>
        <p><b>PAYER ID:</b> <strong><span class="key" id="payerId-value">{payerId}</span></strong></p>
        <p><b>TOKEN:</b> <strong><span class="key" id="token-value">{token}</span></strong></p>
    </div>

</div>

<footer>
    <p>If you have any issues or questions, please contact our support team using the contact info below:<br> </p>
	<div class="page-center">
		<p>Email: jbadonaiventures@gmail.com</p>
		<p>Phone: +234 802 222 4284</p>
	</div>
</footer>

</body>
</html>
"""
    return payment_created_message


async def get_paypal_payment_created_message(email, paymentId, payerId, token):

    style = """    th, td{
    text-align: left;
    background-color: rgb(20,20,20);
    color: rgb(0,225,127);
    border: 1px solid gray;
    }
      table {
    border-collapse: collapse;
    border: 1px solid black;
  }
  h1{
  color:blue;
  }
"""

    payment_created_message =f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <style>
    {style}
  </style>
</head>
<body>
Dear {str(email).split("@")[0]},<br>

 <h1>Thank you for your payment!</h1>
  <p>Here is your receipt for your recent PayPal transaction:</p>
  <table border="1" cellpadding="5px" >
    <tr>
      <th>Transaction ID:</th>
      <td>{paymentId}</td>
    </tr>
    <tr>
      <th>Date:</th>
      <td>{datetime.datetime.today()}</td>
    </tr>
    <tr>
      <th>Paid To:</th>
      <td>JBAdonaiventures International</td>
    </tr>
    <tr>
      <th>Paid By:</th>
      <td>{email}</td>
    </tr>
    <tr>
      <th>Amount:</th>
      <td>${os.environ.get('PAID_LICENSE_AMOUNT')}</td>
    </tr>
    <tr>
      <th>Payment Status:</th>
      <td>Approved!</td>
    </tr>
  </table>
<br><br>
<p>Below information will be required to activate your copy of JVD downloader:</p>
    <div class="card">
         <table border="1" cellpadding="5px">
    <tr>
      <th>PAYMENT ID:</th>
      <td>{paymentId}</td>
    </tr>
    <tr>
      <th>PAYEE ID:</th>
      <td>{payerId}</td>
    </tr>
    <tr>
      <th>TOKEN:</th>
      <td>{token}</td>
    </tr>
  </table>
    <br><br>
    <b>Instruction</b>
    <ul>
    <li> Open JVD downloader, If not already opened.</li>
    <li> Click on 'Buy Full Version' Button, If not already clicked.</li>
    <li> On the 'Payment Confirmation' section, Insert the above data in the appropriate box.</li>
    <li> Then click on 'Confirm Payment And Activate' button.</li>
    <li> Just wait for Payment confirmation and App activation process to complete.</li>

    </ul>

  <p>If you have any questions or concerns, please contact us at jbadonaiventures@gmail.com</p>

</body>
</html>
"""
    return payment_created_message


def get_license_request_message_plain(user, license_key):
    license_request_message =f"""You Are Welcome To Try JBA Video Downloader

Dear {user},
    Thank you for downloading JBA Video Downloader!<br>
    Below is your Free {Config().config("FREE_TRIAL_DAYS")} days Licence code:

    Licence key:

    {license_key}

    To apply Your Free Licence:

            * Open the settings menu by clicking on the gear icon on the tool bar.
            * Paste your licence code in the space provided.
            * Click on 'Activate License' button.

    You are good to go!

"""

    return license_request_message
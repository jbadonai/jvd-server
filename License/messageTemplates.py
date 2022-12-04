from License.environment import Config

async def get_license_request_message(user, license_key):
    days = int(Config().config("FREE_TRIAL_DAYS"))
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
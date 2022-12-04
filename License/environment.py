class Config():
    def __init__(self):
        self.firebaseConfig = {
              'apiKey': "AIzaSyCKIe-C7cLgTcQti7-2sjpY8St0ZHkILXI",
              'authDomain': "video-downloader-auth.firebaseapp.com",
              'databaseURL': "https://video-downloader-auth-default-rtdb.firebaseio.com",
              'projectId': "video-downloader-auth",
              'storageBucket': "video-downloader-auth.appspot.com",
              'messagingSenderId': "98278757450",
              'appId': "1:98278757450:web:3c9752f1e27404c5b802b3",
              'measurementId': "G-J6FR4943V9"
            }
        pass
        # self.config = {
        # "ENCRYPT_PASSWORD": "jbadonaiventures",
        # "HASH_PASSWORD": "jbadoaniventures",
        # "LICENCE_PASSWORD": "jbadonaiventures international",
        # "FREE_TRIAL_DAYS": 2,
        # "CLIENT_ID": "546078638135-kcgf8je6m5idir3g23s83b4t0582nq69.apps.googleusercontent.com",
        # "CLIENT_SECRET": "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",
        # "SCOPES": 'https://www.googleapis.com/auth/gmail.send',
        # "CLIENT_SECRET_FILE": 'client_secret.json',
        # "APPLICATION_NAME": 'Gmail API Video Downloader',
        # "CLIENT_SECRET_RAW": '{"installed":{"client_id":"546078638135-kcgf8je6m5idir3g23s83b4t0582nq69.apps.googleusercontent.com","project_id":"video-downloader-112022","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"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","redirect_uris":["http://localhost"]}}'
        # }

    def config(self, key):

        if key == "FIREBASE_CONFIG": return self.firebaseConfig

        if key == "NO_OF_CLIENTS_ALLOWED_PER_USER": return 2

        if key == "SERVER_ADDRESS": return 'https://downloader-server.herokuapp.com/'
        if key == "LOCAL_SERVER_ADDRESS": return 'http://127.0.0.1:8000/'

        if key == "ENCRYPT_PASSWORD": return "jbadonaiventures"
        if key == "EMAIL_PASSWORD": return "csulnvhscvtwfmaq"
        if key == "EMAIL_ADDRESS": return "jbadonaiventures@gmail.com"
        if key == "ACCESS_PASSWORD": return "afolayemi"
        if key == "HASH_PASSWORD": return "jbadonaiventures"
        if key == "SALT": return "jbadonaiventures"
        if key == "LICENCE_PASSWORD": return "jbadonaiventures international"
        if key == "FREE_TRIAL_DAYS": return 7
        if key == "CLIENT_ID": return "546078638135-kcgf8je6m5idir3g23s83b4t0582nq69.apps.googleusercontent.com"
        if key == "CLIENT_SECRET": return "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"
        if key == "SCOPES": return 'https://www.googleapis.com/auth/gmail.send'
        if key == "CLIENT_SECRET_FILE": return 'f30069d9211e.dll'
        if key == "APPLICATION_NAME": return 'Gmail API Video Downloader'
        if key == "CLIENT_SECRET_RAW": return '{"installed":{"client_id":"546078638135-kcgf8je6m5idir3g23s83b4t0582nq69.apps.googleusercontent.com","project_id":"video-downloader-112022","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"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","redirect_uris":["http://localhost"]}}'


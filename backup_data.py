import firebase_admin
from firebase_admin import credentials, storage
import shutil
import time
import os
import datetime
from PyQt5 import QtCore
import requests

# set default values
sat = os.path.join(os.getcwd(),'routers', 'update.json')
bucket_name = 'video-downloader-auth'


class Backup():
    def __init__(self):
        pass

    async def backup_now(self):

        def check_destination():
            try:
                # Define the destination folder path
                dest_folder_path = 'jvd_server_data_backup'

                # Check if the destination folder exists
                if not os.path.exists(dest_folder_path):
                    # If the folder doesn't exist, create it
                    os.makedirs(dest_folder_path)
                    print(f"Folder '{dest_folder_path}' created successfully.")
                else:
                    print(f"Folder '{dest_folder_path}' already exists.")
            except Exception as e:
                print(e)

        try:
            # Set the path to the Firebase Admin SDK service account key file
            # print("Creating credentials...")
            path = "./routers/update.json"
            cred = credentials.Certificate(path)

            print("initializing firebase....")
            # Initialize the Firebase app with the service account credentials
            # firebase_admin.initialize_app(cred, {
            #     'storageBucket': 'video-downloader-auth.appspot.com'
            #
            # })

            # Get the current date and time
            now = datetime.datetime.now()

            # Format the date and time into a string
            date_string = now.strftime("%Y-%m-%d_%H-%M-%S")

            # Construct the filename with the current date and time
            filename = f"jvd_{date_string}.db"
            filename2 = f"localdb_{date_string}.db"

            print("Defining source and destination file paths...")
            # Define the source and destination file paths
            src_file_path = './jvd.db'
            src_file_path2 = './localdb.db'

            dest_file_path = f'jvd_server_data_backup/{filename}'
            dest_file_path2 = f'jvd_server_data_backup/{filename2}'

            check_destination()

            print("copying...")
            # Copy the source file to the destination folder
            shutil.copy(src_file_path, dest_file_path)
            shutil.copy(src_file_path2, dest_file_path2)

            print("uploading....")
            # Upload the copied file to Firebase storage
            bucket = storage.bucket()
            blob = bucket.blob(dest_file_path)
            blob.upload_from_filename(dest_file_path)

            blob = bucket.blob(dest_file_path2)
            blob.upload_from_filename(dest_file_path2)
            print('Successful! wating for next backup...')

            # remove all existing local backup
            for root, dirs, files in os.walk('jvd_server_data_backup'):
                for file in files:
                    try:
                        os.remove(os.path.join(root, file))
                    except:
                        continue

            return "ok"

        except Exception as e:
            print(e)
            return "nok"


class Restore():
    def __init__(self):
        self.threadController = {}
        self.completed = False
        pass

    async def generate_restore_url(self, filename):
        try:
            global sat, bucket_name
            from google.cloud import storage
            from google.oauth2.service_account import Credentials

            # Load the credentials for your Firebase Storage account
            credentials = Credentials.from_service_account_file(sat)

            # Initialize the Firebase Storage client
            storage_client = storage.Client(credentials=credentials)

            # buckets = list(storage_client.list_buckets())
            # print("Buckets in Firebase Storage:")
            # for bucket in buckets:
            #     print(bucket.name)

            # Get a reference to the file you want to download
            bucket = storage_client.bucket(f"{bucket_name}.appspot.com")

            # generate object name based on platform and latest version
            # version = get_latest_version(platform)  # get the latest version
            # versionMod = version.replace(".", "_")  # mod latest version
            # object_name = f'jvd_updates/windows/version_{version}/JVD_setup_V_{versionMod}.exe'
            object_name = f'jvd_server_data_backup/{filename}'
            blob = bucket.blob(object_name)

            # Generate a signed URL for the file
            url = blob.generate_signed_url(
                version="v4",
                expiration=int(60 * 60),  # URL will be valid for 1 hour
                method="GET",
            )

            # Share the URL with your client
            # print("Download URL:", url)
            return url
        except:
            return None
            pass

    async def restore_now(self, url, save_as_filename):

        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print("Error while trying to download the file: {}".format(e))
            return 'nok'

        try:
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024  # 1 Kibibyte
            written = 0
        except Exception as e:
            print(e)

        try:
            with open(save_as_filename, "wb") as f:
                for data in response.iter_content(block_size):
                    written += len(data)
                    f.write(data)
        except IOError as e:
            print("Error while trying to write the file: {}".format(e))
            return 'nok'

        return "ok"


class DownloadUpdate(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(dict)

    def __init__(self, url):
        super(DownloadUpdate, self).__init__()
        self.url = url
        self.emitData = {}
        pass

    def stop(self):
        self.requestInterruption()

    def download_update(self, url):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print("Error while trying to download the file: {}".format(e))
            exit(1)

        try:
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024  # 1 Kibibyte
            written = 0
        except Exception as e:
            print(e)

        try:
            with open("jvd_setup.exe", "wb") as f:
                for data in response.iter_content(block_size):
                    written += len(data)
                    f.write(data)
                    done = int(100 * written / total_size)
                    self.emitData['done'] = done
                    self.any_signal.emit(self.emitData)
                    # print("\r[{}{}]".format('=' * done, ' ' * (50 - done)), end="")
        except IOError as e:
            print("Error while trying to write the file: {}".format(e))
            exit(1)

    def run(self):
        try:
            self.download_update(self.url)
            self.emitData['completed'] = True
            self.any_signal.emit(self.emitData)
        except Exception as e:
            print(f"An Error Occurred in jvd_updater.py > GetUpdate() > run(): {e}")


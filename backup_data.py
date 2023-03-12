import firebase_admin
from firebase_admin import credentials, storage
import shutil
import time
import os
import datetime


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
            print("Creating credentials...")
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


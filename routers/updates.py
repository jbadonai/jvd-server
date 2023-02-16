from fastapi import APIRouter, Depends, status, HTTPException
import schemas, models, database
from License.security import JBEncrypter, JBHash
from google.cloud import storage
import os
import configparser
import firebase_admin
from firebase_admin import credentials, storage
import time
from exceptionsList import *
# from google.cloud import storage
# from google.oauth2.service_account import Credentials

# set default values
sat = os.path.join(os.getcwd(),'routers', 'update.json')
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = sat
os.environ['LATEST_UPDATE_VERSION'] = "1.0"
latest_update_version = "1.0"
# set bucket name
bucket_name = 'video-downloader-auth'

cred = credentials.Certificate(sat)
firebase_admin.initialize_app(cred, {
    "storageBucket": f"{bucket_name}.appspot.com"
})


# initialize api router
router = APIRouter(
    prefix="/updates",
    tags=["Updates"]
)
get_db = database.get_db    # get database

object_name = 'jvd_updates/windows/version_1.0/version_info.ini'


async def get_latest_version(platform):
    global  bucket_name
    try:
        # ''' platform can either be windows or macOs for now'''
        # if platform != 'windows':
        #     platform = 'macOS'
        # print(bucket_name)
        # cred = credentials.Certificate(sat)
        # firebase_admin.initialize_app(cred, {
        #     "storageBucket": f"{bucket_name}.appspot.com"
        # })

        bucket = storage.bucket()

        # Get a list of all the blobs in the "jvd_updates/windows/" folder
        blobs = bucket.list_blobs(prefix=f"jvd_updates/{platform}/")

        # Create a list to keep track of all the folder names
        folders = []

        # Loop through the blobs and add all the folders to the list
        for blob in blobs:
            if blob.name.endswith("/"):
                folder_name = blob.name[:-1]
                folders.append(folder_name)

        if len(folders) > 1:
            latestVersionFolderName = folders[-1]
            latest_version = str(latestVersionFolderName).split("_")[-1]
            os.environ["LATEST_UPDATE_VERSION"] = latest_version
            latest_update_version = latest_version
            print(f"Latest version is: {latest_version}")
            return latest_version
    except Exception as e:
        latest_update_version = "1.0"
        os.environ["LATEST_UPDATE_VERSION"] = latest_update_version
        return latest_update_version


async def generate_app_download_url(version):
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
        versionMod = version.replace(".", "_")  # mod latest version
        object_name = f'jvd_updates/windows/version_{version}/JVD_setup_V_{versionMod}.exe'
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


def get_file_content():
    bucket = storage.bucket()
    blob = bucket.blob(object_name)

    # Retrieve the contents of the file as a string
    file_content = blob.download_as_string().decode("utf-8")

    # Parse the file contents as an INI file
    config = configparser.ConfigParser()
    config.read_string(file_content)

    '''*SAMPLE*
    [version]
    number=1.0
    release_date=2023-02-10
    '''

    # Use the contents of the file
    print("Version Number:")
    print(config['version']['number'])


def is_authenticated(pp):
    # p = JBHash().hash_message_with_nonce(Config().config('ENCRYPT_PASSWORD'))
    # p = JBHash().hash_message_with_nonce(get_settings('ENCRYPT_PASSWORD'))
    p = JBHash().hash_message_with_nonce(os.environ.get('ENCRYPT_PASSWORD'))
    if pp is None or pp != p[1]:
        return False

    return True


@router.get("", status_code=status.HTTP_200_OK)
async def check_update(current_version: str = "1.0", platform: str = "windows"):
    try:
        latest_version = await get_latest_version(platform)
        if latest_version is None:
            raise OperatingSystemException

        if current_version == latest_version:
            data = {'status_code': status.HTTP_200_OK,
                    'latest_version': latest_version,
                    'url': None,
                    'detail': f"Your application is running the latest update."}
            return data
        elif float(latest_version) > float(current_version):
            # get download url for the latest version
            download_url = await generate_app_download_url(latest_version)
            data = {'status_code': status.HTTP_200_OK,
                    'latest_version': latest_version,
                    'url': download_url,
                    'detail': f"New Update Available."}
            return data
        else:
            download_url = await generate_app_download_url(latest_version)
            data = {'status_code': status.HTTP_200_OK,
                    'latest_version': latest_version,
                    'url': download_url,
                    'detail': f"Available version is {latest_version}. You may have to switch to this version."}
            return data
    except OperatingSystemException:
        data = {'status_code': status.HTTP_406_NOT_ACCEPTABLE,
                'latest_version': None,
                'url': None,
                'detail': f"Unsupported OS: {platform}"}
        return data
    except Exception as e:
        data = {'status_code': status.HTTP_406_NOT_ACCEPTABLE,
                'latest_version': None,
                'url': None,
                'detail': f"Error: {str(e)}"}
        return data


# version = get_latest_version("windows")
# generate_app_download_url(version)
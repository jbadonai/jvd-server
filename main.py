try:
    from fastapi import FastAPI, status, HTTPException
    from database import engine
    import models
    import database
    from routers import client, user, license, payments, updates
    import uvicorn
    import  os
    import  time
    from License import security
    from localDatabase import LocalDatabase
    import platform
    from setup import ServerSetUP
    from License.security import JBEncrypter, JBHash
    from backup_data import Backup, Restore
except Exception as e:
    print(f"An Error Occurred in imports section: {e}")
    input("press any key to terminate")

app = FastAPI(docs_url="/jbadonaiventures/jesus_is_lord/bible/john_3_16", redoc_url=None)

app.include_router(client.router)
app.include_router(user.router)
app.include_router(license.router)
app.include_router(payments.router)
app.include_router(updates.router)

models.Base.metadata.create_all(engine)
get_db = database.get_db()

configuration_data = None


def is_authenticated(pp):
    p = JBHash().hash_message_with_nonce(os.environ.get('ENCRYPT_PASSWORD'))
    if pp is None or pp != p[1]:
        return False

    return True


@app.get("/", status_code=status.HTTP_200_OK)
def home():
    return {'status': f'Welcome Home!'}


@app.get("/backup", status_code=status.HTTP_200_OK)
async def backup():
    try:
        result = await Backup().backup_now()

        if result == 'ok':
            return {'status': "Successful"}
        else:
            return {'status': "Failed to Backup"}
    except Exception as e:
        return {'status': f"Backup failed: {e} "}


@app.get("/restore", status_code=status.HTTP_200_OK)
async def restore(filename: str=""):
    try:
        if filename == "":
            raise Exception

        url = await Restore().generate_restore_url(filename)

        if url is None:
            raise Exception

        save_as_filename = f"{str(filename).split('_')[0]}.db"
        result = await Restore().restore_now(url, save_as_filename)

        if result == 'ok':
            return {'status': "Successful"}
        else:
            return {'status': "Failed to Restore"}
    except Exception as e:
        return {'status': f"Restoration failed: {e} "}


@app.get("/config/get", status_code=status.HTTP_200_OK)
def load_config(pp: str=None):
    global configuration_data

    if is_authenticated(pp) is False:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Not Authorized")

    if configuration_data is not None:
        encConfigData = {}
        for data in configuration_data:
            val = configuration_data[data]
            valEnc = JBEncrypter().encrypt(str(val))
            # key = JBEncrypter().encrypt(data)
            encConfigData[data] = valEnc

        return {'data': encConfigData}
    else:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Not Authorized")

def clear_screen():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')


if __name__ == "__main__":

    def initialize():
        global configuration_data
        try:
            server_setup = ServerSetUP()
            # check main database file
            print("checking if database file exists...")
            if os.path.exists('jvd.db') is False:
                print("Creating main database...")
                with open('jvd.db', 'w') as fp:
                    pass

            while True:
                print("Checking database file ...")
                if os.path.exists('jvd.db') is True:
                    break
                time.sleep(1)

            #   initialize local server settings database
            print("Initializing settings database...")
            LocalDatabase().initialize_database()

            # get config setting from fb
            print("Getting configuration data from data server")
            server_setup.intialize_setup()
            myConfig = server_setup.config_data

            # configuration = security.get_config()
            # myConfig = configuration[0]
            # errorDetail = configuration[1]

            #   save the configruation  from fb to server settings database

            if myConfig is not None:
                print('Saving configuration data')
                configuration_data = myConfig

                for config in myConfig:
                    # check if the key exists in the database
                    settingExists = LocalDatabase().is_setting_key_in_database(config)

                    if settingExists is False:
                        # if key does not exist create a new one
                        val = myConfig[config]
                        valEnc = JBEncrypter().encrypt(str(val))
                        LocalDatabase().setup_create_settings(config, valEnc)
                    else:
                        # if key exists updated it with new one from fb
                        val = myConfig[config]
                        valEnc = JBEncrypter().encrypt(str(val))
                        LocalDatabase().update_setting(config, valEnc)

                return True
            else:
                print(f"No configuration data found on data server: \n\tError detail:-{errorDetail}")
                return False
        except Exception as e:
            print(f"Last attemp: {e}")
            return False
            pass

    def start():
        result = initialize()
        if result is True:
            uvicorn.run(app, host='127.0.0.1', port=8000)
        else:
            print('Unable to start Server! No configuration data was received form data Server')
            # check if there is an existing data to work with locally and seek users concent to continue with it or not.
            test = LocalDatabase().is_setting_key_in_database('ENCRYPT_PASSWORD')
            # val = LocalDatabase().get_settings('ENCRYPT_PASSWORD')
            val = os.environ.get('ENCRYPT_PASSWORD')
            if test is True and val is not None:
                ans = input("An Old data was found! Continue with old data? (y/n): ")
                if ans == 'y' or ans == 'Y':
                    uvicorn.run(app, host='127.0.0.1', port=8000)
                else:
                    print()
                    print("Try again later when the internet has been restored.")
                    ans = input("Press any key to exit or 'R' to restart:")
                    if ans == "R":
                        clear_screen()
                        start()

    start()


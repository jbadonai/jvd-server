try:
    from fastapi import FastAPI, status
    from database import engine
    import models
    import database
    from routers import client, user, license
    import uvicorn
    import  os
    import  time
    from License import security
    from localDatabase import LocalDatabase
    from License.security import JBEncrypter
except Exception as e:
    print(f"An Error Occurred in imports section: {e}")
    input("press any key to terminate")

print("Initializing completed!")

app = FastAPI(docs_url="/jbadonaiventures/jesus_is_lord/bible/john_3_16", redoc_url=None)

app.include_router(client.router)
app.include_router(user.router)
app.include_router(license.router)

models.Base.metadata.create_all(engine)
get_db = database.get_db()


@app.get("/", status_code=status.HTTP_200_OK)
def home():
    return {'status': 'Welcome Home!'}


if __name__ == "__main__":

    def initialize():
        try:
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
            myConfig = security.get_config()[0]
            errorDetail = security.get_config()[1]

            #   save the configruation  from fb to server settings database

            if myConfig is not None:
                print('Saving configuration data')
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

    result = initialize()
    if result is True:
        uvicorn.run(app, host='127.0.0.1', port=8000)
    else:
        print('Unable to start Server! No configuration data was received form data Server')

        # check if there is an existing data to work with locally and seek users concent to continue with it or not.
        test = LocalDatabase().is_setting_key_in_database('ENCRYPT_PASSWORD')
        if test is True:
            ans = input("An Old data was found! Continue with old data? (y/n): ")
            if ans == 'y' or ans == 'Y':
                uvicorn.run(app, host='127.0.0.1', port=8000)
            else:
                print()
                print("Try again later when the internet has been restored.")


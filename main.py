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
            myConfig = security.get_config()

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
                print("No configuration data found on data server")
                return False
        except:
            return False
            pass

    result = initialize()
    if result is True:
        uvicorn.run(app, host='127.0.0.1', port=8000)
    else:
        print('Unable to start Server! No configuration data was received form data Server')


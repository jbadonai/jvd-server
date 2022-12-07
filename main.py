from fastapi import FastAPI, status
from database import engine
import models
import database
from routers import client, user, license
import uvicorn
from License.security import JBEncrypter
from License.environment import Config


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
    uvicorn.run(app, host='127.0.0.1', port=8000)


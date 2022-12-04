from fastapi import FastAPI, status
from database import engine
import models
import database
from routers import client, user, license
import uvicorn


app = FastAPI()

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


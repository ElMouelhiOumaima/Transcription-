from fastapi import FastAPI
from uvicorn import Config, Server
from configuration.config import MicroserviceSettings,DB_URL
from fastapi_sqlalchemy import DBSessionMiddleware
from app.routes import database
from app.routes import transcription
host = MicroserviceSettings.HOST
port = MicroserviceSettings.PORT
app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=DB_URL)
app.include_router(database.router)
app.include_router(transcription.router)

@app.get("/")
async def read_main():
    return {"msg": "Hello World"}

if __name__ == '__main__':
     server = Server(Config(app=app, host=host, port=port))
     server.run()
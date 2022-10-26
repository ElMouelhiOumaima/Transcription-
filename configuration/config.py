from pydantic import BaseSettings , Field
class MicroserviceConfiguration(BaseSettings):
    HOST: str =Field("0.0.0.0", env="HOST")
    PORT: int = Field("8110", env="PORT")
    DB_NAME: str = Field(default="dialect_transcription_db",env="DB_NAME")
    DB_USER: str = Field(default="postgres",env="DB_USER")
    DB_NAME_test: str = Field(default="transcription_db_test",env="DB_NAME_test")
    DB_PASSWORD: str = Field(env="DB_PASSWORD", default="password")
    # DB_HOST: str = Field(env="DB_HOST", default="localhost")
    DB_HOST: str = Field(env="DB_HOST", default="postgresql_dial_transcription")
    DB_HOST_test: str = Field(env="DB_HOST", default="postgresql_test_transcription")
    DB_PORT: int = Field(env="DB_PORT", default=5432)
    PGADMIN_EMAIL :str = Field(env="PGADMIN_EMAIL",default="admin@admin.com")
    PGADMIN_PASSWORD: str = Field(env="PGADMIN_PASSWORD", default="admin")
MicroserviceSettings = MicroserviceConfiguration()
DB_URL= f"postgresql://{MicroserviceSettings.DB_USER}:{MicroserviceSettings.DB_PASSWORD}@{MicroserviceSettings.DB_HOST}:{MicroserviceSettings.DB_PORT}/{MicroserviceSettings.DB_NAME}"
DB_URL_test= f"postgresql://{MicroserviceSettings.DB_USER}:{MicroserviceSettings.DB_PASSWORD}@{MicroserviceSettings.DB_HOST_test}:{MicroserviceSettings.DB_PORT}/{MicroserviceSettings.DB_NAME_test}"
    

    



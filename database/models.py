from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from configuration.config import DB_URL as SQLALCHEMY_DATABASE_URL
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Audio(Base):
    '''Table containing information about the audio to be transcripted'''
    __tablename__ = "Audios"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    transcription = Column(String)
    dialect = Column(String,server_default="EGY")
    duration = Column(Integer)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    # audio_id = Column(Integer)
    # owner_id = Column(Integer, ForeignKey("Owner.id"))
    # owner = relationship("Owner")
    
class Owner(Base):
    '''Table containing information about the owner of the audio to be transcripted'''
    __tablename__ = "Owner"
    id = Column(Integer, primary_key=True)
    name = Column(String)


engine = create_engine(SQLALCHEMY_DATABASE_URL,echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(engine)  

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

import wave
from fastapi import APIRouter,UploadFile,Depends,HTTPException,status,File
from sqlalchemy.orm import Session
import contextlib
from vosk import Model
from app.services.kaldi_service import decode_kaldi
from loguru import logger
import shutil
from database.models import Audio
from database.models import get_db
from app.services.transcription_fct import transcription_model
router = APIRouter()

@router.post("/uploadfiletotranscription")
def transcription_upload_file(file: UploadFile,db: Session = Depends(get_db)):
   with open(f'{file.filename}', "wb") as buffer:
      shutil.copyfileobj(file.file, buffer)
   buffer.close()
   with contextlib.closing(wave.open(file.filename,'r')) as f:
    frames = f.getnframes()
    rate = f.getframerate()
    duration = round(frames / float(rate))
    a = Audio()
    a.duration=duration
    a.name=file.filename
    a.transcription=transcription_model(str(file.filename))
    db.add(a)
    db.commit()
    db.refresh(a)
   return transcription_model(str(file.filename))
   
@router.post('/kaldi/transcript')
def transcribe(file: UploadFile = File(...),db: Session = Depends(get_db)):
    """
    This function transcribe an audio file
    :arg file : Audio file in wav format
    :returns transcription json
    """
    
    model = Model("vosk_ar")
    logger.info('Starting transcription')
    with open(f"{file.filename}", 'wb') as f:
        shutil.copyfileobj(file.file, f)
    with contextlib.closing(wave.open(file.filename,'r')) as f:
      frames = f.getnframes()
      rate = f.getframerate()
      duration = round(frames / float(rate))   
      a = Audio()
      a.duration=duration
      a.name=file.filename
      a.transcription=decode_kaldi(model, file)
      db.add(a)
      db.commit()
      db.refresh(a)    
   
    return True
   #  try:
   #      return 

   #  except Exception as error:
   #      logger.error("Error occurred : {}".format(error))
   #      raise HTTPException(status.HTTP_400_BAD_REQUEST)
      

  
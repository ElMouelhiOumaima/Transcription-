from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from database.models import get_db
from database.models import Audio,Owner
from schema import Audio_Update

class DbApisQueries:
    @staticmethod
    def add_audio(audio:Audio,db: Session = Depends(get_db)) :
        '''this function adds a an audio
    return:
    audio : information about the audio'''
        new_data = Audio(**audio.dict())
        db.add(new_data)
        db.commit()
        db.refresh(new_data)

        return new_data
    @staticmethod
    def add_owner(owner: Owner,db: Session = Depends(get_db)) :
        '''this function adds a new owner 
    return:
    owner :information of the owner added recently'''
        new_data = Owner()
        new_data.name = owner.name
        new_data.id=owner.id
        db.add(new_data)
        db.commit()
        db.refresh(new_data)
        return new_data
    
    @staticmethod    
    def get_all(db: Session = Depends(get_db)):
        '''get all the information about the audios'''
        return db.query(Audio).all()
   
    @staticmethod    
    def get_all_owner(db: Session = Depends(get_db)):
        '''get all the information about the OWNERS'''
        return db.query(Owner).all()
    @staticmethod      
    def update_audio(name:str,updated_audio: Audio_Update,db: Session = Depends(get_db)):
        ''' update audio information'''   
     
        audio_query = db.query(Audio).filter(Audio.name == name)
        audio = audio_query.first() 
        if audio == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"audio with name: {name} does not exist")
        audio_query.update(updated_audio.dict(), synchronize_session=False)
        db.commit()
        return updated_audio
    @staticmethod
    def get_audio_name(name:str,db: Session = Depends(get_db)) :
        ''' get information of the audio depending on its name '''
        audio_query = db.query(Audio).filter(Audio.name == name)
        audio = audio_query.first() 
        if audio == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"audio with name: {name} does not exist")
        return audio                    
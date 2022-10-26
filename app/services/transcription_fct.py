from klaam.run import SpeechRecognition
def transcription_model(audio_file_name: str):
   return SpeechRecognition().transcribe(audio_file_name)

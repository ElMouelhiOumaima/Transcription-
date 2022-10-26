import ast
import time
import wave
import ffmpy
from loguru import logger
from vosk import KaldiRecognizer, Model
from fastapi import UploadFile,File
from app.services.tools import clean
from data.data_schema import TranscriptionResponse
def convert_16k_mono(path: str, output_sample_rate: str = '16000', clear: bool = True) -> str or None:
    """
    convert a stereo audiofile with x sampling rate to a mono audiofile with 16000 sampling rate
    The previous file will be overwritten
    :param path: to audio file
    :param output_sample_rate
    :param clear: clear the file after the conversion
    """
    
    try:
        # Convert to mono 16k sample, log only errors
        ff = ffmpy.FFmpeg(
            inputs={path: None},
            outputs={path + '_16k_mono.wav': ['-ac', '1', '-ar', output_sample_rate,
                                              '-hide_banner', '-loglevel', 'error', '-y']})
        ff.run()
    except Exception as error:
        logger.error("Something went wrong during conversion : {}".format(error))
        clean(path)
        return None
    if clear:
        clean(path)
    return path 


def decode_kaldi(model: Model, file: UploadFile = File(...)) -> TranscriptionResponse or None:
    """
    pass bytes to kaldi recognizer object, and return a transcription
    :param model: Vosk model
    :param file: FastAPI path
    :return:
    """
    
    convert_16k_mono(file.filename)
    response = TranscriptionResponse()
    wave_file = wave.open(file.filename+"_16k_mono.wav", "rb")
    rec = KaldiRecognizer(model, wave_file.getframerate())
    rec.SetWords(True)

    time_start = time.time()

    while True:
        data = wave_file.readframes(4000)
        if len(data) == 0:
            break
        else:
            rec.AcceptWaveform(data)

    evaluated = ast.literal_eval(rec.FinalResult())
    if "result" not in evaluated:
        evaluated["result"] = []
    try:
        response.words.extend(evaluated["result"])
        response.text += evaluated["text"] + " "
    except Exception as error:
        logger.error('Error occurred : {}'.format(error))
        return None
    decoding_time = (time.time() - time_start)
    logger.debug("Decoding took %8.2fs" % decoding_time)
    return response.text
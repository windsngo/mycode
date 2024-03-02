from pydub import AudioSegment
import os
from pydub.silence import split_on_silence
import speech_recognition as sr
import sys
def transcribe(filePath, language ):
  sound = AudioSegment.from_file(filePath)
  chunks = split_on_silence(sound, min_silence_len=500, silence_thresh=sound.dBFS-14, keep_silence=500)
  os.makedirs('audio_chunks', exist_ok=True)
  count=0
  for chunk in chunks:
    temp_filePath = f'audio_chunks/{count}.wav'
    chunk.export(temp_filePath, format='wav')
    r = sr.Recognizer()
    with sr.AudioFile(temp_filePath) as source:
      listened_audio = r.record(source)
      try:
        text = r.recognize_google(listened_audio, language=language)
      except sr.UnknownValueError:
        print('ERROR!!!')
      else:
        print(text)
if __name__ == '__main__':
  filePath = sys.argv[1]
  language = sys.argv[2]
  transcribe(filePath, language)
  

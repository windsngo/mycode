import os
from pydub import AudioSegment
from pytube import YouTube
import speech_recognition as sr
from pydub.silence import split_on_silence
def download_and_translate_audio_yt(url, filename):
  audio = YouTube(url)
  output = audio.streams.get_audio_only().download()
  new_file = filename + '.mp4'
  os.rename(output, new_file)
  src = new_file
  dst = filename + '.wav'
  sound = AudioSegment.from_file(src, format='mp4')
  sound.export(dst, format="wav")

r = sr.Recognizer()

def transcribe_audio(path):
    with sr.AudioFile(path) as source:
        audio_listened = r.record(source)
        text = r.recognize_google(audio_listened)
    return text
def get_large_audio_transcription_on_silence(path):
    sound = AudioSegment.from_file(path)
    chunks = split_on_silence(sound,
        min_silence_len = 500,
        silence_thresh = sound.dBFS-14,
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    data = {}
    error = {}
    for i, audio_chunk in enumerate(chunks, start=1):
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        try:
            text = transcribe_audio(chunk_filename)
        except sr.UnknownValueError as e:
            error[chunk_filename]  = str(e)
        else:
            text = f"{text.capitalize()}. "
            data[chunk_filename] = text
    return data, error

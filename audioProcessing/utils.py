import os
import io
from django.conf import settings
import speech_recognition as sr  # wav파일만 처리 가능
import googletrans
from gtts import gTTS


def audio_to_text(audio):
    """
    audio -> text

    :param audio: 한국어 음성 파일
    :return: 음성 인식 결과 text
    """
    r = sr.Recognizer()
    read_audio = sr.AudioFile(audio)
    with read_audio as source:
        f = r.record(source)
    out_text = r.recognize_google(f, language="ko-KR")
    return out_text


def text_translate(in_text):
    """
    kr_text -> en_text

    :param in_text: 한국어 text
    :return: 영어로 번역된 text
    """
    translator = googletrans.Translator()
    out_text = translator.translate(in_text, dest='en').text
    return out_text


def text_to_tts(in_text):
    """
    en_text -> tts(wav file)

    :param in_text: tts로 읽을 텍스트
    :return: tts wav file
    """
    tts = gTTS(text=in_text, lang='en')
    wav_data = io.BytesIO()
    tts.write_to_fp(wav_data)
    return wav_data


def rename_audio_file(pk, audio_data, audio_type):
    """
    Rename the audio file associated with the AudioData model.

    :param pk: primary key of AudioData model instance
    :param audio_data: processed/original audio data of AudioData model instance
    :param audio_type: 'processed' or 'original'
    :return: None
    """
    initial_path = audio_data.path
    if audio_type == 'processed':
        audio_data.name = f"processed/{pk}_processed.wav"
    else:
        audio_data.name = f"original/{pk}.wav"
    new_path = settings.MEDIA_ROOT / audio_data.name
    os.rename(initial_path, new_path)
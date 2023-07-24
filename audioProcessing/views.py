from django.shortcuts import render, redirect
from .forms import AudioForm
from django.utils import timezone
from .utils import *

'''
1. 타 음성파일 -> wav로 변환 과정 추가 필요
'''


def main(request):
    if request.method == 'POST':
        form = AudioForm(request.POST, request.FILES)
        if form.is_valid():
            audio_data = form.save(commit=False)
            audio_data.create_date = timezone.now()
            audio_file = request.FILES['original_audio']

            # 한국어 음성 -> 텍스트 변환
            kr_text = audio_to_text(audio_file)
            audio_data.original_text = kr_text

            # 한 -> 영 텍스트 번역
            en_text = text_translate(kr_text)
            audio_data.processed_text = en_text

            # tts wav file create
            tts_file = text_to_tts(en_text)
            audio_data.processed_audio.save(audio_file.name, tts_file)

            # original file rename
            rename_audio_file(audio_data.pk, audio_data.original_audio, 'original')

            # processed file rename
            rename_audio_file(audio_data.pk, audio_data.processed_audio, 'processed')

            audio_data.save()
            context = {'form': form, 'audio_data': audio_data}
            return render(request, 'main.html', context)
    else:
        form = AudioForm()
    context = {'form': form}
    return render(request, 'main.html', context)

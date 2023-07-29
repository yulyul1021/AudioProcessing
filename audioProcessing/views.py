from django.shortcuts import render
from .forms import AudioForm
from django.utils import timezone
from .utils import *

from django.core.files.uploadedfile import InMemoryUploadedFile # 녹음으로 input 되었을 때 check용


def main(request):
    if request.method == 'POST':
        form = AudioForm(request.POST, request.FILES)
        if form.is_valid():
            audio_data = form.save(commit=False)
            audio_data.create_date = timezone.now()

            if not request.FILES.get('original_audio'):
                # 텍스트만 input -> 번역 -> tts
                kr_text = audio_data.original_text

                # 한 -> 영 텍스트 번역
                en_text = text_translate(kr_text)
                audio_data.processed_text = en_text

                # tts wav file create
                tts_file = text_to_tts(en_text)
                audio_data.processed_audio.save(f'temp{audio_data.pk}.wav', tts_file)

                # processed file rename
                rename_audio_file(audio_data.pk, audio_data.processed_audio, 'processed')

            elif not request.POST.get('original_text'):
                # 오디오만 input -> 인식 -> 번역 -> tts
                audio_file = request.FILES['original_audio']

                # 녹음으로 들어왔을때 데이터 변환
                if isinstance(audio_file, InMemoryUploadedFile):
                    wav_file = request.FILES['original_audio'].file
                    audio_data.original_audio.save(audio_file.name, wav_file) # 정상적으로 저장 및 재생됨
                    audio_file = wav_file
                #

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

            # else:
                # 둘 다 input ->

            audio_data.save()
            context = {'form': form, 'audio_data': audio_data}
            return render(request, 'main.html', context)
    else:
        form = AudioForm()
    context = {'form': form}
    return render(request, 'main.html', context)

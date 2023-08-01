from django.shortcuts import render
from .forms import AudioForm
from django.utils import timezone
from .utils import *


def index(request):
    if request.method == 'POST':
        form = AudioForm(request.POST, request.FILES)
        if form.is_valid():
            audio_data = form.save(commit=False)
            audio_data.create_date = timezone.now()

            if request.FILES.get('original_audio') and request.POST.get('original_text'):
                # 나중에 수정하기
                audio_file = request.FILES['original_audio']

                # 한국어 음성 -> 텍스트 변환
                kr_text = audio_data.original_text  # 녹음된 파일일시 해당 함수에서 오류

                # 한 -> 영 텍스트 번역
                en_text = text_translate(kr_text)
                # audio_data.processed_text = en_text

                # tts wav file create
                tts_file = text_to_tts(en_text)
                audio_data.processed_audio.save(audio_file.name, tts_file)

                # original file rename
                rename_audio_file(audio_data.pk, audio_data.original_audio, 'original')

                # processed file rename
                rename_audio_file(audio_data.pk, audio_data.processed_audio, 'processed')

            elif not request.POST.get('original_text'):
                # 오디오만 input -> 인식 -> 번역 -> tts
                audio_file = request.FILES['original_audio']

                # 한국어 음성 -> 텍스트 변환
                kr_text = audio_to_text(audio_file)  # 녹음된 파일일시 해당 함수에서 오류
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

            else:
                # 텍스트만 input -> 번역 -> tts
                kr_text = audio_data.original_text

                # 한 -> 영 텍스트 번역
                en_text = text_translate(kr_text)
                audio_data.processed_text = en_text

                # tts wav file create and save
                tts_file = text_to_tts(en_text)
                audio_data.processed_audio.save(f'temp{audio_data.pk}.wav', tts_file)

                # processed file rename
                rename_audio_file(audio_data.pk, audio_data.processed_audio, 'processed')

            audio_data.save()
            context = {'form': form, 'audio_data': audio_data}
            return render(request, 'index.html', context)
    else:
        form = AudioForm()
    context = {'form': form}
    return render(request, 'index.html', context)

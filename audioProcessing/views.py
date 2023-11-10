from django.shortcuts import render
from .forms import AudioForm
from django.utils import timezone
from .utils import *
from .models import AudioData
import soundfile as sf


def index(request):
    if request.method == 'POST':
        form = AudioForm(request.POST, request.FILES)
        if form.is_valid():
            audio_data = form.save(commit=False)
            audio_data.create_date = timezone.now()

            if request.FILES.get('original_video'):
                # video input
                video_file = request.FILES['original_video']
                wav_file = mp4_to_wav(video_file)
                request.FILES['original_audio'] = wav_file
                # TODO 비디오 wav로 변환 -> 오디오로 넘기기

            if request.FILES.get('original_audio'):  # 오디오만 input
                audio_file = request.FILES['original_audio']

                vad = WebRTCVAD()
                num_audios, onsets, offsets, crop_audios, wav_audios = vad.detect_endpoints(audio_file)

                google_sr = SpeechRecognition()
                texts = google_sr.recognize_korean(num_audios=num_audios)

                for i in range(num_audios):
                    kr_text = texts[i]
                    en_text = text_translate(kr_text)
                    tts_file = text_to_tts(en_text)

                    tmp = AudioData(create_date=audio_data.create_date,
                                    original_text=kr_text, processed_text=en_text,
                                    onset=onsets[i], offset=offsets[i])

                    tmp.original_audio.save(audio_file.name, wav_audios[i])
                    rename_audio_file(tmp.pk, tmp.original_audio, 'original')
                    tmp.processed_audio.save(audio_file.name, tts_file)
                    rename_audio_file(tmp.pk, tmp.processed_audio, 'processed')

                    tmp.save()


            '''
            if request.FILES.get('original_audio') and request.POST.get('original_text'):
                # 오디오, 텍스트 둘 다 입력 / 나중에 수정하기
                audio_file = request.FILES['original_audio']

                # 한국어 음성 -> 텍스트 변환
                kr_text = audio_data.original_text

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
                '''

            if not request.FILES.get('original_audio'):
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

            audio_data = AudioData.objects.filter(create_date=audio_data.create_date)
            context = {'form': form, 'audio_data': audio_data}
            return render(request, 'index.html', context)
    else:
        form = AudioForm()
    context = {'form': form}
    return render(request, 'index.html', context)

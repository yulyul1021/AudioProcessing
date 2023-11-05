from django import forms
from audioProcessing.models import AudioData


class AudioForm(forms.ModelForm):
    class Meta:
        model = AudioData
        fields = ['original_video', 'original_audio', 'original_text']
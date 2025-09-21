from django import forms
from .models import VoiceRecord

class SymptomForm(forms.Form):
    text = forms.CharField(label='', widget=forms.Textarea(attrs={"rows": 4, "placeholder":"Semptomlarınızı ve şikayetlerinizi yazınız"}))
    disease_length = forms.CharField(label='', widget=forms.Textarea(attrs={"rows": 2, "placeholder":"Şikayetlerinizin kaç gündür devam ettiğini yazınız"}))


class VoiceRecordForm(forms.ModelForm):
    class Meta:
        model = VoiceRecord
        fields = ['audio_file']
        labels = {'audio_file': ''}
        widgets = {
            'audio_file': forms.ClearableFileInput(attrs={
                'class': 'block w-full text-sm text-gray-700 border border-gray-300 rounded-lg cursor-pointer focus:ring-blue-500 focus:border-blue-500',
                'accept': 'audio/*',
                'label': ''
            }),
        }
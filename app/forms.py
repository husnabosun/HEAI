from django import forms

class SymptomForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={"rows": 4, "placeholder":"Semptomlarınızı ve şikayetlerinizi yazınız"}))
    disease_length = forms.CharField(widget=forms.Textarea(attrs={"rows": 2, "placeholder":"Şikayetlerinizin kaç gündür devam ettiğini yazınız"}))
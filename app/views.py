from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from app.models import MyUser
from .forms import SymptomForm
from openai import OpenAI
import os
import json
import string
from huggingface_hub import InferenceClient
from dotenv import load_dotenv


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, '.env'))


client = OpenAI(api_key=(os.getenv("OPENAI_API_KEY")))
hf_client = InferenceClient(token=os.getenv("HF_TOKEN"))

def register(request):
    if request.method == "POST":
        tc = request.POST.get('tc')
        password = request.POST.get('password')
        if tc and password:
            MyUser.objects.create_user(tc=tc, password=password)
            print("başarı")
            return redirect('login')
    return render(request, 'login.html')

def user_login(request):
    if request.method == "POST":
        tc = request.POST.get('tc')
        password = request.POST.get('password')
        user = authenticate(request, tc=tc, password=password)
        if user is not None:
            login(request, user)
            print("başarı")
            return redirect('symptom_input')
        else:
            print("failure")
            return render(request, 'login.html', {'error': 'T.C. veya şifre hatalı'})
    return render(request, 'login.html')


def symptom_input(request):
    output_to_show = None
    disease_predict = None
    recommended_branch = None 
    if request.method == "POST":
        form = SymptomForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
            ai_response = extract_symptoms(text)
            
            output_to_show = ai_response_view(ai_response)
            
            disease_predict = predict_disease(ai_response)[:3]
            
            recommended_branch = determine_branch([i[0] for i in disease_predict])
    else:
        form = SymptomForm()
    
    return render(request, "symptom_form.html", {"form": form, "output_to_show" : output_to_show, "disease_predict": disease_predict, "recommended_branch": recommended_branch})

    
def extract_symptoms(user_text):
    prompt = (f"Translate the following text to English and extract only the symptoms mentioned, separated by commas."
    f"If the text does not contain any valid symptoms or is nonsensical, respond with no valid symptoms found"
    f"Do not include extra words, sentences, or repetitions. Output should be only a single line of symptoms. Text: '{user_text}'")
    
    symptom_response = call_gpt(prompt)
    
    return symptom_response


def ai_response_view(ai_response):
    prompt = (f"Translate the text to Turkish Text: '{ai_response}'")
    
    symptoms_turkish = string.capwords(call_gpt(prompt))
    
    return symptoms_turkish

def call_gpt(prompt):
    response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
    temperature=0
    )
    return response.choices[0].message.content


def predict_disease(symptoms):
    result = hf_client.text_classification(
        symptoms,
        model="shanover/symps_disease_bert_v3_c41",
    )
    
    with open("config.json") as f:
        config = json.load(f)

    id2label = config["id2label"]
    

    output = []
    for i in result:
        label_id = i["label"].replace("LABEL_", "")
        real_name = id2label[label_id] 
        prompt = (f"Translate this disease in Turkish: {real_name}")
        
        disease_in_turkish = call_gpt(prompt)
        
        output.append([
            disease_in_turkish,
            (f"{round(i['score']*100, 3)}%")
        ])
    
    return output

def determine_branch(disease):
    disease_branch_list = []
    for i in disease:
        prompt = (f"Recommend the most appropriate medical department or specialty for this disease in just in turkish."
            f"Respond in a single line in the following format:"
            f"{i} İçin Tavsiye Edilen Departman: ... . The diseases is: {i}")
        disease_branch = call_gpt(prompt)
        disease_branch_list.append(disease_branch)
    
    return disease_branch_list

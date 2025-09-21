from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.conf import settings
from app.models import MyUser, SymptomRecord, VoiceRecord
from .forms import SymptomForm, VoiceRecordForm
from openai import OpenAI
from transformers import pipeline
from django.contrib import messages
import os
import whisper
import pymupdf
import pandas as pd
import json
import string
import csv
from datetime import datetime, timedelta
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))


client = OpenAI(api_key=(os.getenv("OPENAI_API_KEY")))
hf_client = InferenceClient(token=os.getenv("HF_TOKEN"))


def register(request):
    if request.method == "POST":
        tc = request.POST.get("tc")
        password = request.POST.get("password")
        if not tc or not password:
            messages.error(request, "T.C. kimlik numarası ve şifre zorunludur.")
            return render(request, "user_login.html")
        
        # TC kontrolü
        if len(tc) != 11 or not tc.isdigit():
            messages.error(request, "T.C. kimlik numarası 11 haneli olmalı ve sadece rakam içermelidir.")
            return render(request, "user_login.html")
        
        # Kullanıcı zaten var mı kontrol et
        if MyUser.objects.filter(tc=tc).exists():
            messages.error(request, "Bu T.C. kimlik numarası ile zaten kayıtlı bir kullanıcı var.")
            return render(request, "user_login.html")
        
        try:
            MyUser.objects.create_user(tc=tc, password=password)
            messages.success(request, "Kayıt başarılı! Giriş yapabilirsiniz.")
            print("Kayıt başarılı")
            return redirect("user_login")
        except Exception as e:
            messages.error(request, f"Kayıt sırasında hata oluştu: {str(e)}")
            return render(request, "user_login.html")
    
    return render(request, "user_login.html")



def user_login(request):
    if request.method == "POST":
        tc = request.POST.get("tc")
        password = request.POST.get("password")
        
        print(f"tc: {tc}, password: {password}") 
        
        if not tc or not password:
            messages.error(request, "T.C. kimlik numarası ve şifre zorunludur.")
            return render(request, "user_login.html")
        
        user = authenticate(request, tc=tc, password=password)
        print(f"user: {user}")
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Hoş geldiniz!")
            print("Giriş başarılı")
            return redirect("symptom_input")
        else:
            messages.error(request, "T.C. kimlik numarası veya şifre hatalı.")
            print("Giriş başarısız")
            return render(request, "user_login.html")
    
    return render(request, "user_login.html")


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
            
            with open("mock_records.csv", mode="a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([
                    datetime.now().strftime("%Y-%m-%d"), 
                    output_to_show,                                
                    disease_predict[0][0],                        
                    recommended_branch[0].split(":")[1].strip(),                                                          # risk_level (örnek)
                ])
            
            SymptomRecord.objects.create(symptoms=output_to_show, disease=disease_predict[0][0], branch=recommended_branch[0])
            
            
    else:
        form = SymptomForm()

    return render(
        request,
        "symptom_form.html",
        {
            "form": form,
            "output_to_show": output_to_show,
            "disease_predict": disease_predict,
            "recommended_branch": recommended_branch,
        },
    )


def extract_symptoms(user_text):
    prompt = (
        f"Translate the following text to English and extract only the symptoms mentioned, separated by commas."
        f"If the text does not contain any valid symptoms or is nonsensical, respond with no valid symptoms found"
        f"Do not include extra words, sentences, or repetitions. Output should be only a single line of symptoms. Text: '{user_text}'"
    )

    symptom_response = call_gpt(prompt)

    return symptom_response


def ai_response_view(ai_response):
    prompt = f"Translate the text to Turkish Text: '{ai_response}'"

    symptoms_turkish = string.capwords(call_gpt(prompt))

    return symptoms_turkish


def call_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return response.choices[0].message.content


def predict_disease(symptoms):
    pipe = pipeline("text-classification", model="shanover/symps_disease_bert_v3_c41", return_all_scores=True )
    response = pipe(symptoms)
    result = sorted(response[0], key=lambda x: x["score"], reverse=True)[:3]

    with open("config.json") as f:
        config = json.load(f)

    id2label = config["id2label"]

    output = []
    for i in result:
        label_id = i["label"].replace("LABEL_", "")
        real_name = id2label[label_id]
        prompt = f"Translate this disease in Turkish: {real_name}"

        disease_in_turkish = call_gpt(prompt)

        output.append([disease_in_turkish, (f"{round(i['score']*100, 2)}%")])

    return output


def determine_branch(disease):
    disease_branch_list = []
    for i in disease:
        prompt = (
            f"Recommend the most appropriate medical department or specialty for this disease in just in turkish."
            f"Respond in a single line in the following format:"
            f"{i} İçin Tavsiye Edilen Departman: ... . The diseases is: {i}"
        )
        disease_branch = call_gpt(prompt)
        disease_branch_list.append(disease_branch)

    return disease_branch_list


@csrf_exempt
def ai_treatment(request):
    if request.method == "POST":
        data = json.loads(request.body)
        diseases = data.get("diseases", [])

        recommendations = []

        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)

            mild_conditions = config["mild_conditions"]
            serious_conditions = config["serious_conditions"]

        for i in diseases:
            prompt = None
            if i.lower() in mild_conditions:
                prompt = f"""
            You are a medical assistant.
            A patient has the following disease: {i}.
            Give practical treatment recommendations in Turkish, as if explaining to a patient at home.
            Symptoms are mild, emphasize rest, hydration, and simple measures.
            - Give 2–3 specific actionable suggestions (for example: “Dinlen, sıcak çay iç, gerekirse doktora başvur”).
            - Format output like this: 
            {i} İçin Tedavi Önerileri: <recommendations>
            - Do not just translate English recommendations; generate context-specific, natural Turkish advice.
            """

            elif i.lower() in serious_conditions:
                prompt = f"""
            You are a medical assistant.
            A patient has the following disease: {i}.
            Give practical treatment recommendations in Turkish, as if explaining to a patient at home.
            Emphasize that symptoms are serious and the patient should arrange a doctor appointment. 
            Tell that if the patient requests, an online meeting can be arranged with an online health consultant before the doctor appointment.
            - Give 2–3 specific actionable suggestions ..
            - Format output like this: 
            {i} İçin Tedavi Önerileri: <recommendations>
            - Do not just translate English recommendations; generate context-specific, natural Turkish advice.
            """



            if prompt is None:
                continue
            response = call_gpt(prompt)
            recommendations.append(response)

        return JsonResponse({"recommendations": recommendations})

def trend_data(request):
    csv_path = os.path.join(settings.BASE_DIR, "mock_records.csv")
    df = pd.read_csv(csv_path)
    
    today = datetime.strptime("2025-09-14", "%Y-%m-%d").date()
    
    df['created_at'] = pd.to_datetime(df['created_at']).dt.date
    
    week_ago = today - timedelta(days=6)
    
    df = df[(df['created_at'] >= week_ago) & (df['created_at'] <= today)]
    
    df['date_str'] = df['created_at'].apply(lambda x: x.strftime("%Y-%m-%d"))
    
    disease_counts = df.groupby(['date_str', 'disease']).size().unstack(fill_value=0)
    
    branch_counts = df.groupby(['date_str', 'branch']).size().unstack(fill_value=0)

    all_symptoms = {}
    for _, row in df.iterrows():
        for symptom in row['symptoms'].split(", "):
            if symptom not in all_symptoms:
                all_symptoms[symptom] = {}
            date_str = row['date_str']
            all_symptoms[symptom][date_str] = all_symptoms[symptom].get(date_str, 0) + 1

    
    dates = pd.date_range(start=week_ago, end=today).strftime("%Y-%m-%d").tolist()

    
    symptom_counts = {}
    for symptom, counts in all_symptoms.items():
        symptom_counts[symptom] = [counts.get(date, 0) for date in dates]

    data = {
        "dates": dates,
        "disease_counts": {d: disease_counts[d].reindex(dates, fill_value=0).tolist() for d in disease_counts.columns},
        "branch_counts": {b: branch_counts[b].reindex(dates, fill_value=0).tolist() for b in branch_counts.columns},
        "symptom_counts": symptom_counts,
    }
    return JsonResponse(data)
    
def charts(request):
    return render(request, "charts.html")




def get_df(request):
    return render(request, "get_df.html")


def upload_view(request):
    df_list = []
    test_results = []
    column_names = None
    
    if request.method == "POST":
        raw_doc = request.FILES['pdf_file']
        doc = pymupdf.open(stream=raw_doc.read(), filetype='pdf')
        page = doc[0]
        tables = (page.find_tables()).tables

        if tables:
            table = tables[0]
            raw_data = table.extract()
            # df = table.to_pandas()

            column_names = raw_data[0]
            data = raw_data[1:]


            df = pd.DataFrame(data, columns=column_names)

            df_list.append(df)
        
            full_df = pd.concat(df_list, ignore_index=True)
            without_date_filtered_df = full_df.drop(columns='Tarih').iloc[:20]
            
            
            for i in range(20):
                name = without_date_filtered_df.loc[i]['Tahlil']
                if '<' in without_date_filtered_df.loc[i]['Sonuç']:
                    result = without_date_filtered_df.loc[i]['Sonuç']
                else:
                    if ',' in without_date_filtered_df.loc[i]['Sonuç']:
                        result = float(without_date_filtered_df.loc[i]['Sonuç'].replace(",", "."))
                    else:                    
                        result = float(without_date_filtered_df.loc[i]['Sonuç'])
                    
                health_range = without_date_filtered_df.loc[i]['Referans\nDeğeri']
                
                a = {'Tahlil' : name, 'Sonuç' : result, 'Referans Değeri': health_range}
                test_results.append(a)
            print(test_results)
            request.session["test_results"] = test_results
            
            return redirect("get_df")
        
    return render(request, "upload_view.html")

def upload_data(request):
    data = request.session.get("test_results", [])
    print(data)
    return JsonResponse(data, safe=False)



def upload_voice(request):
    model = whisper.load_model("small", device="cpu")
    if request.method == 'GET':
        form = VoiceRecordForm()
        return render(request, 'upload_voice.html', {'form': form})

    if request.method == 'POST':
        form = VoiceRecordForm(request.POST, request.FILES)
        if form.is_valid():
            voice = form.save(commit=False)
            voice.save()

            audio_path = voice.audio_file.path
            result = model.transcribe(audio_path)
            transcript_text = result["text"]
            
            
            prompt = f"""
            Verilen hasta-doktor diyalogunu oku ve yapılandırılmış bir özet çıkar. Özet aşağıdaki bölümleri içermeli:

            1. Hastanın ana şikayetleri ve genel durumu.
            2. Doktorun verdiği her ilacı ayrı ayrı listele. Her ilacın:
            - Hangi şikayeti tedavi ettiği
            - Olası hafif yan etkileri
            3. Doktorun ilaç dışında verdiği öneriler (dinlenme, sıvı tüketimi, dikkat edilmesi gerekenler)
            4. Doktorun hastaya hangi durumlarda tekrar gelmesini söylediği
            5. Özet, hastaya hitap bazlı olacak şekilde yazılsın; örneğin "Boğaz ağrınız olduğunu belirttiniz, doktor Tylol hod reçete etti ve ..." gibi.
                Diyalog: {transcript_text}"""


            response = call_gpt(prompt)
            
            voice.summary = response  
            voice.save()

            return JsonResponse({'summary': voice.summary})
        
        else:
            return JsonResponse({'error': 'Form geçersiz'}, status=400)
    else:
        form = VoiceRecordForm()
        return render(request, 'upload_voice.html', {'form': form}) 



def appointment_summary(request):
    voice_records = VoiceRecord.objects.all() 
    return render(request, 'appointment_summary.html', {'voice_records': voice_records})


def contact_view(request):
    return render(request, 'contact.html')

@login_required
def profile_view(request):
    user = request.user  
    return render(request, "profile.html", {"user": user})


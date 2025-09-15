import csv
import random
from datetime import datetime, timedelta

common_diseases = [
    "Soğuk Algınlığı",
    "Alerji",
    "Migren",
    "Gastroenterit",
    "Bronşiyal Astım",
    "İdrar Yolu Enfeksiyonu",
]

branches = {
    "Soğuk Algınlığı": "Dahiliye",
    "Alerji": "KBB",
    "Migren": "Nöroloji",
    "Gastroenterit": "Gastroenteroloji",
    "Bronşiyal Astım": "Göğüs Hastalıkları",
    "İdrar Yolu Enfeksiyonu": "Üroloji",
}

symptoms_dict = {
    "Soğuk Algınlığı": ["öksürük", "burun akıntısı", "hapşırık"],
    "Alerji": ["burun tıkanıklığı", "kaşıntı", "hapşırık"],
    "Migren": ["baş ağrısı", "ışığa hassasiyet", "bulantı"],
    "Gastroenterit": ["ishal", "karın ağrısı", "bulantı"],
    "Bronşiyal Astım": ["nefes darlığı", "öksürük", "hırıltı"],
    "İdrar Yolu Enfeksiyonu": ["idrar yaparken ağrı", "sık idrara çıkma", "yanma hissi"],
}

weights = [40, 30, 10, 10, 5, 5]
with open("mock_records.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["created_at", "symptoms", "disease", "branch"])

    for _ in range(100):  
        disease = random.choices(common_diseases,weights=weights, k=1)[0]
        symptoms = symptoms = symptoms_dict[disease]

        created_at = (datetime.now() - timedelta(days=random.randint(0,7))).strftime("%Y-%m-%d")

        writer.writerow([created_at, ", ".join(symptoms), disease, branches[disease]])

print("mock_records.csv dosyası oluşturuldu!")

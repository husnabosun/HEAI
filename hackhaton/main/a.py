from openai import OpenAI

client = OpenAI(api_key="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")

def extract_symptoms(user_text):
    prompt = f"Kullanıcının metninden sadece semptomları çıkart. Metin: '{user_text}'"
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    
    return response.choices[0].message.content

# Örnek
user_text = "Boğazım ağrıyor, hafif ateşim var ve biraz halsizim"
symptoms = extract_symptoms(user_text)
print(symptoms)

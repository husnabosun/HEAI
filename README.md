# HEAI – Sağlık ve Yapay Zeka Destekli Analiz Sistemi

**HEAI**, modern web teknolojileri ve yapay zekayı birleştirerek, hastalık tespiti, tahlil analizi ve hasta-doktor iletişimini tek bir platformda sunan kapsamlı bir sağlık uygulamasıdır.

## Kullanılan Teknolojiler

- **Backend:** Django  
- **Frontend:** HTML, CSS, JavaScript, Tailwind  
- **Veri Analizi:** Pandas (tahlil sonuçlarının işlenmesi ve uygun aralıkların kontrolü)  
- **PDF İşleme:** PyMuPDF (tahlil sonuçlarını PDF’den tabloya çevirme)  
- **Grafikler:** Chart.js (yayılım trendleri ve analiz görselleştirmeleri)  
- **Yapay Zeka:** Hugging Face GPT ve Whisper (hastalık tespiti, tahlil özetleri, görüşme özetleri)  

## Temel Özellikler

1. **Kayıt ve Giriş:** TC ve şifre ile güvenli kullanıcı kaydı ve login.  
2. **Şikayet Formu:** Formdan alınan semptomlara göre Hugging Face modeli ile hastalık tespiti.  
3. **Tavsiye ve Öneriler:** Tespit edilen hastalıklara uygun öneriler ve medikal bilgilendirme.  
4. **Yayılım Trendleri:** Semptom girişlerinden oluşturulan CSV dosyaları ile trend grafikler; en popüler 3 yayılım için AI önerileri.  
5. **Tahlil Sonuçları:** PDF yükleme → tabloya çevirme → değerlerin uygunluğunu gözlemleme → hormonlar hakkında genel bilgi (MedicalPoint).  
6. **Hasta-Doktor Görüşmesi:** Ses kaydı ile görüşme → Whisper ile metne çevirme → yapay zekadan özet ve doktor önerisi → database’e kaydetme ve hastaya gösterme.  

## Teknik Notlar

- OpenAI ve Hugging Face API anahtarları güvenlik nedeniyle `.env` dosyasında saklanmakta ve projede paylaşılmamaktadır.  
- Tüm veriler güvenli şekilde işlenir ve analizler gerçek zamanlı olarak grafiklere yansıtılır.  

## Kurulum ve Çalıştırma

1. Depoyu klonlayın:  
```bash
git clone https://github.com/husnabosun/HEAI.git
cd HEAI
````
2. Sanal ortam oluşturun:  
```bash
python -m venv venv
venv\Scripts\activate # Windows için
```
3. Gerekli paketleri yükleyin:  
```bash
pip install -r requirements.txt
```
4. .env dosyanızı oluşturun ve API anahtarlarını ekleyin::  
```bash
OPENAI_API_KEY=your_openai_key
HF_TOKEN=your_hf_key
```
5. Veritabanı migrasyonlarını uygulayın:  
```bash
python manage.py makemigrations
python manage.py migrate
```
6. Sunucuyu başlatın:  
```bash
python manage.py runserver
```
7. Tarayıcıda açın:  
```bash
http://127.0.0.1:8000
```
8. Admin paneline erişim ve veri görüntüleme için superuser oluşturun ve komutları takip edin:
```bash
python manage.py createsuperuser
```

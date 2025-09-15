import pandas as pd
import matplotlib.pyplot as plt


# CSV oku
df = pd.read_csv("mock_records.csv", parse_dates=["created_at"])

# Sadece son 7 gün
last_week = df[df["created_at"] >= pd.Timestamp.now() - pd.Timedelta(days=7)]

# Günlük sayım: Hastalık bazlı
disease_trend = last_week.groupby([last_week["created_at"].dt.date, "disease"]).size().unstack(fill_value=0)

# Grafik çiz
plt.figure(figsize=(12,6))
disease_trend.plot(kind="line", marker="o")
plt.title("Son 1 Haftada Hastalık Eğilimleri")
plt.xlabel("Tarih")
plt.ylabel("Vaka Sayısı")
plt.xticks(rotation=45)
plt.legend(title="Hastalık", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()
plt.show()
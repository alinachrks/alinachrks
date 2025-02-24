import os
import sys
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# 🔧 Настройки
USERNAME = "alinachrks"  # Замените на свой Codewars username
API_URL = f"https://www.codewars.com/api/v1/users/{USERNAME}"
OUTPUT_DIR = "output"

# 🔍 Дебаг-лог
print("✅ Starting Codewars analytics generation...")
print(f"Python version: {sys.version}")
print(f"Current working directory: {os.getcwd()}")

# 📂 Создаём папку для сохранения файлов
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 📡 Запрос к Codewars API
response = requests.get(API_URL)
if response.status_code != 200:
    print(f"❌ ERROR: Failed to fetch data from Codewars API ({response.status_code})")
    sys.exit(1)

data = response.json()

# 📊 Извлечение данных
rank = data.get("ranks", {}).get("overall", {}).get("name", "N/A")
honor = data.get("honor", 0)
challenges_completed = data.get("codeChallenges", {}).get("totalCompleted", 0)
languages = data.get("ranks", {}).get("languages", {})

print(f"🏆 Rank: {rank}, Honor: {honor}, Completed Challenges: {challenges_completed}")

# 📈 Данные для графиков
history_file = os.path.join(OUTPUT_DIR, "codewars_progress.csv")
if os.path.exists(history_file):
    df = pd.read_csv(history_file)
else:
    df = pd.DataFrame(columns=["date", "honor", "challenges_completed"])

# 🔄 Добавление новых данных
df = df.append({"date": datetime.utcnow().strftime("%Y-%m-%d"), "honor": honor, "challenges_completed": challenges_completed}, ignore_index=True)
df.to_csv(history_file, index=False)

# 📊 **График роста Honor Points**
plt.figure(figsize=(8, 5))
sns.lineplot(data=df, x="date", y="honor", marker="o", color="purple")
plt.xlabel("Date")
plt.ylabel("Honor Points")
plt.title("Growth of Honor Points")
plt.xticks(rotation=45)
plt.grid(True)
plt.savefig(os.path.join(OUTPUT_DIR, "codewars_graph.svg"), format="svg")
plt.close()

# 🥇 **Круговая диаграмма решённых задач по рангам**
ranks = {lang: info["name"] for lang, info in languages.items()}
plt.figure(figsize=(6, 6))
plt.pie([1] * len(ranks), labels=[f"{lang} ({r})" for lang, r in ranks.items()], autopct="%1.1f%%", colors=sns.color_palette("coolwarm", len(ranks)))
plt.title("Solved Challenges by Rank")
plt.savefig(os.path.join(OUTPUT_DIR, "codewars_pie.svg"), format="svg")
plt.close()

# 🔥 **Тепловая карта активности по дням**
heatmap_data = df.pivot_table(values="challenges_completed", index="date", aggfunc="sum").fillna(0)
plt.figure(figsize=(8, 4))
sns.heatmap(heatmap_data, cmap="OrRd", linewidths=0.1, linecolor="gray")
plt.title("Weekly Activity Heatmap")
plt.savefig(os.path.join(OUTPUT_DIR, "codewars_heatmap.svg"), format="svg")
plt.close()

# 📊 **Гистограмма решённых задач по языкам**
plt.figure(figsize=(8, 5))
sns.barplot(x=list(ranks.keys()), y=[1] * len(ranks), palette="viridis")
plt.xlabel("Languages")
plt.ylabel("Challenges Solved")
plt.title("Challenges per Language")
plt.xticks(rotation=45)
plt.savefig(os.path.join(OUTPUT_DIR, "codewars_barchart.svg"), format="svg")
plt.close()

print("✅ All analytics generated and saved successfully!")

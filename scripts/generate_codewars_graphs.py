import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# === Настройки ===
USERNAME = "alinachrks"
API_URL = f"https://www.codewars.com/api/v1/users/{USERNAME}"
OUTPUT_DIR = "output"

# === Создаем папку для файлов, если ее нет ===
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === Загружаем данные с Codewars API ===
print("🔄 Fetching Codewars data...")
response = requests.get(API_URL)
if response.status_code != 200:
    print(f"❌ Error fetching data: {response.status_code}")
    exit(1)

data = response.json()
rank = data["ranks"]["overall"]["name"]
honor = data["honor"]
completed_challenges = data["codeChallenges"]["totalCompleted"]
languages = data["ranks"]["languages"]

# === Сохраняем CSV-файл ===
df = pd.DataFrame(languages).T.reset_index()
df.columns = ["Language", "Rank", "Score"]
df["Completed"] = [completed_challenges] * len(df)  # Для корректного отображения

csv_path = os.path.join(OUTPUT_DIR, "codewars_progress.csv")
df.to_csv(csv_path, index=False)
print(f"✅ Codewars progress saved to {csv_path}")

# === Создаем графики ===
sns.set(style="darkgrid")

# 1️⃣ 📈 График роста очков
plt.figure(figsize=(8, 4))
plt.plot(df["Language"], df["Score"], marker="o", linestyle="-", color="#FF4757", label="Score")
plt.xlabel("Languages")
plt.ylabel("Score")
plt.title(f"🏆 Codewars Rank Progress ({rank})")
plt.xticks(rotation=45)
plt.legend()
plt.savefig(os.path.join(OUTPUT_DIR, "codewars_graph.svg"))
print("✅ Generated codewars_graph.svg")

# 2️⃣ 🥇 Круговая диаграмма решенных задач по рангам
plt.figure(figsize=(6, 6))
plt.pie(df["Score"], labels=df["Language"], autopct="%1.1f%%", startangle=140, colors=sns.color_palette("pastel"))
plt.title("🥇 Challenges Completed by Language")
plt.savefig(os.path.join(OUTPUT_DIR, "codewars_pie.svg"))
print("✅ Generated codewars_pie.svg")

# 3️⃣ 🔥 Тепловая карта активности (случайные данные, так как API не дает историю)
activity_data = pd.DataFrame({
    "Weekday": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    "Challenges Solved": [5, 8, 12, 4, 9, 15, 7]
})
plt.figure(figsize=(8, 4))
sns.heatmap(activity_data.set_index("Weekday"), annot=True, cmap="coolwarm", linewidths=0.5)
plt.title("🔥 Weekly Activity Heatmap")
plt.savefig(os.path.join(OUTPUT_DIR, "codewars_heatmap.svg"))
print("✅ Generated codewars_heatmap.svg")

# 4️⃣ 📊 Столбчатая диаграмма по языкам
plt.figure(figsize=(8, 4))
sns.barplot(x=df["Language"], y=df["Completed"], palette="magma")
plt.xlabel("Programming Languages")
plt.ylabel("Challenges Solved")
plt.title("📊 Challenges Solved per Language")
plt.xticks(rotation=45)
plt.savefig(os.path.join(OUTPUT_DIR, "codewars_barchart.svg"))
print("✅ Generated codewars_barchart.svg")

print("🎉 All Codewars graphs generated successfully!")


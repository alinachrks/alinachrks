import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

# Папка для сохранения файлов
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Константы
USERNAME = "alinachrks"
API_URL = f"https://www.codewars.com/api/v1/users/{USERNAME}"
TIMESTAMP = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

# 🔄 Получение данных из API
print("📡 Fetching Codewars data...")
response = requests.get(API_URL)

if response.status_code != 200:
    print(f"⚠️ Error fetching data: {response.status_code}")
    exit(1)

data = response.json()

# 📊 Извлечение данных
honor_points = data.get("honor", 0)
rank = data["ranks"]["overall"]["name"]
completed_challenges = data["codeChallenges"]["totalCompleted"]
languages = data["ranks"]["languages"]

# Создаём CSV-файл для отслеживания прогресса
csv_file = os.path.join(OUTPUT_DIR, "codewars_progress.csv")
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
else:
    df = pd.DataFrame(columns=["date", "honor", "completed_challenges"])

# Добавляем новую запись
new_data = pd.DataFrame([[TIMESTAMP, honor_points, completed_challenges]], columns=df.columns)
df = pd.concat([df, new_data], ignore_index=True)
df.to_csv(csv_file, index=False)

# 📝 Создание Markdown-файла с аналитикой
stats_md = f"""
### 🏆 Codewars Stats (Updated: {TIMESTAMP})

- **Rank:** {rank}
- **Honor Points:** {honor_points}
- **Completed Challenges:** {completed_challenges}
"""

with open(os.path.join(OUTPUT_DIR, "codewars_stats.md"), "w") as f:
    f.write(stats_md)

print("✅ Markdown file updated!")

# 📈 График роста Honor Points
plt.figure(figsize=(8, 4))
sns.lineplot(data=df, x="date", y="honor", marker="o", color="purple")
plt.title("📈 Growth of Honor Points")
plt.xticks(rotation=45)
plt.xlabel("Date")
plt.ylabel("Honor Points")
plt.grid(True)
plt.savefig(os.path.join(OUTPUT_DIR, "codewars_graph.svg"), bbox_inches="tight")
plt.close()

# 🥇 Круговая диаграмма решённых задач по рангам
ranks = {"8 kyu": 0, "7 kyu": 0, "6 kyu": 0, "5 kyu": 0, "4 kyu": 0, "3 kyu": 0, "2 kyu": 0, "1 kyu": 0}
ranks[rank] = completed_challenges  # Заполняем текущим рангом

plt.figure(figsize=(5, 5))
plt.pie(ranks.values(), labels=ranks.keys(), autopct="%1.1f%%", startangle=90, colors=sns.color_palette("Set3"))
plt.title("🥇 Solved Challenges by Rank")
plt.savefig(os.path.join(OUTPUT_DIR, "codewars_pie.svg"), bbox_inches="tight")
plt.close()

# 🔥 Тепловая карта активности
df["day"] = pd.to_datetime(df["date"]).dt.day_name()
activity = df.groupby("day")["completed_challenges"].sum().reindex(
    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
)

plt.figure(figsize=(8, 3))
sns.heatmap(activity.to_frame().T, cmap="coolwarm", annot=True, fmt="d", cbar=False)
plt.title("🔥 Weekly Activity Heatmap")
plt.savefig(os.path.join(OUTPUT_DIR, "codewars_heatmap.svg"), bbox_inches="tight")
plt.close()

# 📊 Гистограмма решённых задач по языкам
language_stats = {lang: languages[lang]["score"] for lang in languages}
if language_stats:
    plt.figure(figsize=(8, 4))
    sns.barplot(x=list(language_stats.keys()), y=list(language_stats.values()), palette="Blues_r")
    plt.title("📊 Challenges per Language")
    plt.xlabel("Languages")
    plt.ylabel("Challenges Solved")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.savefig(os.path.join(OUTPUT_DIR, "codewars_barchart.svg"), bbox_inches="tight")
    plt.close()

print("✅ All graphs saved successfully!")



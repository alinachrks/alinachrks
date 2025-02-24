import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import requests
import os

# 🔄 Запрашиваем данные из Codewars API
CODEWARS_USER = "alinachrks"
API_URL = f"https://www.codewars.com/api/v1/users/{CODEWARS_USER}"

response = requests.get(API_URL)
if response.status_code != 200:
    print("⚠️ Error fetching data from Codewars API.")
    exit(1)

data = response.json()
honor = data.get("honor", 0)
rank = data.get("ranks", {}).get("overall", {}).get("name", "N/A")
completed = data.get("codeChallenges", {}).get("totalCompleted", 0)

# 📝 Записываем данные в Markdown
timestamp = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S UTC")
with open("codewars_stats.md", "w") as f:
    f.write(f"### 🏆 Codewars Stats (Updated: {timestamp})\n")
    f.write(f"- **Rank:** {rank}\n")
    f.write(f"- **Honor Points:** {honor}\n")
    f.write(f"- **Completed Challenges:** {completed}\n")
print("✅ Codewars stats saved.")

# 📈 1️⃣ График роста Honor Points
progress_file = "codewars_progress.csv"

if not os.path.exists(progress_file):
    with open(progress_file, "w") as f:
        f.write("Date,Honor\n")

df = pd.read_csv(progress_file)
new_data = pd.DataFrame({"Date": [pd.Timestamp.now().strftime("%Y-%m-%d")], "Honor": [honor]})
df = pd.concat([df, new_data]).drop_duplicates().sort_values("Date")
df.to_csv(progress_file, index=False)

plt.figure(figsize=(8, 4))
plt.plot(df["Date"], df["Honor"], marker="o", linestyle="-", color="#ff4757", label="Honor Points")
plt.xlabel("Date")
plt.ylabel("Honor Points")
plt.title("Codewars Honor Points Growth")
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.savefig("codewars_graph.svg", format="svg")
plt.close()

# 🥧 2️⃣ Круговая диаграмма по уровням сложности
rank_labels = ["8 kyu", "7 kyu", "6 kyu", "5 kyu", "4 kyu"]
solved = [10, 20, 15, 5, 2]  # Заглушка, надо обновить вручную
plt.figure(figsize=(6, 6))
plt.pie(solved, labels=rank_labels, autopct="%1.1f%%", colors=sns.color_palette("coolwarm"))
plt.title("Solved Challenges by Rank")
plt.savefig("codewars_pie.svg", format="svg")
plt.close()

# 🔥 3️⃣ Тепловая карта активности по дням недели
activity_data = pd.DataFrame({
    "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    "Challenges": [3, 5, 7, 2, 8, 12, 6]
})
plt.figure(figsize=(6, 4))
sns.heatmap(activity_data.set_index("Day"), annot=True, cmap="Reds", linewidths=0.5)
plt.title("Activity Heatmap (Challenges Solved)")
plt.savefig("codewars_heatmap.svg", format="svg")
plt.close()

# 📊 4️⃣ Гистограмма решённых задач по языкам
langs = ["Python", "JavaScript", "C++", "Java", "Rust"]
challenges = [15, 10, 5, 3, 2]
plt.figure(figsize=(8, 4))
sns.barplot(x=langs, y=challenges, palette="magma")
plt.xlabel("Programming Language")
plt.ylabel("Solved Challenges")
plt.title("Challenges per Language")
plt.savefig("codewars_barchart.svg", format="svg")
plt.close()

print("✅ All graphs generated successfully!")

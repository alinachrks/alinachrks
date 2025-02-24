import os

import sys
sys.stdout.reconfigure(encoding='utf-8')

import matplotlib
matplotlib.use("Agg")  # Используем без GUI

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import requests
import json

# Конфигурация API
USERNAME = "alinachrks"
API_URL = f"https://www.codewars.com/api/v1/users/{USERNAME}"
OUTPUT_DIR = "."  # Корень ветки output

# Проверяем, существует ли папка output
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Запрос данных
try:
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()  # Вызывает ошибку, если статус-код не 200
    data = response.json()
except requests.exceptions.RequestException as e:
    print(f"⚠️ Failed to fetch data from Codewars API: {e}")
    exit(1)

# Проверка наличия данных
if "honor" not in data or "ranks" not in data or "codeChallenges" not in data:
    print("⚠️ Codewars API returned incomplete data.")
    exit(1)

# Извлекаем данные
honor_points = data.get("honor", 0)
rank = data["ranks"]["overall"].get("name", "Unknown")
challenges_completed = data["codeChallenges"].get("totalCompleted", 0)

# Сохранение данных в CSV
df = pd.DataFrame([{
    "Honor Points": honor_points,
    "Rank": rank,
    "Completed Challenges": challenges_completed
}])

df.to_csv(os.path.join(OUTPUT_DIR, "codewars_stats.csv"), index=False)

# 📊 График роста очков Honor
plt.figure(figsize=(6, 3))
sns.barplot(x=["Honor Points"], y=[honor_points], palette="coolwarm")
plt.title("Codewars Honor Points")
plt.ylabel("Points")
plt.savefig(os.path.join(OUTPUT_DIR, "codewars_graph.svg"), format="svg")
plt.close()

# 🥇 Pie Chart - Решенные задачи по уровням
plt.figure(figsize=(4, 4))
plt.pie([challenges_completed, max(1, 100 - challenges_completed)], 
        labels=["Completed", "Remaining"], 
        autopct="%1.1f%%", colors=["#ff4757", "#dfe4ea"])
plt.title("Solved Challenges")
plt.savefig(os.path.join(OUTPUT_DIR, "codewars_pie.svg"), format="svg")
plt.close()

# 🔥 Heatmap (заглушка, можно улучшить под реальные данные)
heatmap_data = pd.DataFrame({
    "Week": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    "Activity": [1, 3, 5, 2, 6, 4, 7]
})
plt.figure(figsize=(6, 3))
sns.heatmap(heatmap_data.set_index("Week"), annot=True, cmap="coolwarm")
plt.title("Weekly Codewars Activity")
plt.savefig(os.path.join(OUTPUT_DIR, "codewars_heatmap.svg"), format="svg")
plt.close()

# 📊 Bar Chart - Разбитие по языкам (если есть данные)
if "languages" in data["ranks"] and data["ranks"]["languages"]:
    languages = list(data["ranks"]["languages"].keys())
    scores = [data["ranks"]["languages"][lang]["score"] for lang in languages]

    plt.figure(figsize=(6, 3))
    sns.barplot(x=languages, y=scores, palette="magma")
    plt.title("Challenges Per Language")
    plt.xlabel("Programming Language")
    plt.ylabel("Score")
    plt.savefig(os.path.join(OUTPUT_DIR, "codewars_barchart.svg"), format="svg")
    plt.close()
else:
    print("⚠️ No language data available in Codewars API.")

print("✅ Codewars analytics generated successfully!")

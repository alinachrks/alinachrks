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

# Запрос данных
response = requests.get(API_URL)
if response.status_code != 200:
    print("⚠️ Failed to fetch data from Codewars API")
    exit(1)

data = response.json()

# Извлекаем данные
honor_points = data["honor"]
rank = data["ranks"]["overall"]["name"]
challenges_completed = data["codeChallenges"]["totalCompleted"]

# Сохранение данных в CSV
df = pd.DataFrame([{"Honor Points": honor_points, "Rank": rank, "Completed Challenges": challenges_completed}])
df.to_csv(os.path.join(OUTPUT_DIR, "codewars_stats.csv"), index=False)

# 📊 График роста очков Honor
plt.figure(figsize=(6, 3))
sns.barplot(x=["Honor Points"], y=[honor_points], palette="coolwarm")
plt.title("Codewars Honor Points")
plt.savefig(os.path.join(OUTPUT_DIR, "codewars_graph.svg"), format="svg")

# 🥇 Pie Chart - Решенные задачи по уровням
plt.figure(figsize=(4, 4))
plt.pie([challenges_completed, 100 - challenges_completed], labels=["Completed", "Remaining"], autopct="%1.1f%%", colors=["#ff4757", "#dfe4ea"])
plt.title("Solved Challenges")
plt.savefig(os.path.join(OUTPUT_DIR, "codewars_pie.svg"), format="svg")

# 🔥 Heatmap (заглушка, можно допилить для активности по дням)
heatmap_data = pd.DataFrame({"Week": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], "Activity": [1, 3, 5, 2, 6, 4, 7]})
plt.figure(figsize=(6, 3))
sns.heatmap(heatmap_data.set_index("Week"), annot=True, cmap="coolwarm")
plt.title("Weekly Codewars Activity")
plt.savefig(os.path.join(OUTPUT_DIR, "codewars_heatmap.svg"), format="svg")

# 📊 Bar Chart - Разбитие по языкам (пока одно значение)
plt.figure(figsize=(6, 3))
sns.barplot(x=["Python"], y=[honor_points], palette="magma")
plt.title("Challenges Per Language")
plt.savefig(os.path.join(OUTPUT_DIR, "codewars_barchart.svg"), format="svg")

print("✅ Codewars analytics generated successfully!")

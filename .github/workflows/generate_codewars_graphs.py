import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import os

# 🔧 Настройки
USERNAME = "alinachrks"
API_URL = f"https://www.codewars.com/api/v1/users/{USERNAME}"
OUTPUT_DIR = "./"  # Хранилище файлов (оставить в корне)

# 🎯 Создаем папку, если ее нет
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_codewars_stats():
    """ Получает статистику Codewars через API """
    response = requests.get(API_URL)
    if response.status_code != 200:
        print(f"⚠️ API request failed! Status: {response.status_code}")
        return None

    data = response.json()
    stats = {
        "rank": data["ranks"]["overall"]["name"],
        "honor": data["honor"],
        "completed_challenges": data["codeChallenges"]["totalCompleted"],
        "languages": data["ranks"].get("languages", {})
    }
    return stats

def save_csv(stats):
    """ Сохраняет статистику в CSV """
    csv_file = os.path.join(OUTPUT_DIR, "codewars_progress.csv")
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    df = pd.DataFrame([{
        "date": timestamp,
        "rank": stats["rank"],
        "honor": stats["honor"],
        "completed_challenges": stats["completed_challenges"]
    }])

    # Дописываем в файл, если он уже существует
    if os.path.exists(csv_file):
        df.to_csv(csv_file, mode='a', header=False, index=False)
    else:
        df.to_csv(csv_file, index=False)

    print(f"✅ Saved stats to {csv_file}")

def generate_graphs():
    """ Генерирует графики из CSV """
    csv_file = os.path.join(OUTPUT_DIR, "codewars_progress.csv")
    if not os.path.exists(csv_file):
        print("⚠️ No data to generate graphs!")
        return

    df = pd.read_csv(csv_file)
    df["date"] = pd.to_datetime(df["date"])

    # 📈 График роста Honor Points
    plt.figure(figsize=(8, 4))
    sns.lineplot(data=df, x="date", y="honor", marker="o", color="red")
    plt.title("📈 Growth of Honor Points")
    plt.xticks(rotation=45)
    plt.savefig(os.path.join(OUTPUT_DIR, "codewars_graph.svg"), bbox_inches="tight")
    plt.close()

    # 🥇 Pie Chart - Решенные задачи по рангу
    plt.figure(figsize=(6, 6))
    sizes = [df["completed_challenges"].iloc[-1], df["honor"].iloc[-1]]
    labels = ["Completed Challenges", "Honor Points"]
    colors = ["#ff4757", "#ff9f43"]
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", colors=colors, startangle=90)
    plt.title("🥇 Solved Challenges by Rank")
    plt.savefig(os.path.join(OUTPUT_DIR, "codewars_pie.svg"), bbox_inches="tight")
    plt.close()

    # 🔥 Heatmap - Активность по неделям
    df["week"] = df["date"].dt.strftime("%Y-%U")
    heatmap_data = df.groupby("week").sum()["completed_challenges"].unstack(fill_value=0)

    plt.figure(figsize=(8, 3))
    sns.heatmap(heatmap_data.T, cmap="coolwarm", linewidths=0.5, annot=True)
    plt.title("🔥 Weekly Activity Heatmap")
    plt.savefig(os.path.join(OUTPUT_DIR, "codewars_heatmap.svg"), bbox_inches="tight")
    plt.close()

    print("✅ Graphs generated successfully!")

def generate_bar_chart(stats):
    """ Генерирует столбчатую диаграмму по языкам """
    languages = stats["languages"]
    if not languages:
        print("⚠️ No language data found!")
        return

    lang_names = list(languages.keys())
    lang_ranks = [int(languages[lang]["rank"]) for lang in lang_names]

    plt.figure(figsize=(8, 4))
    sns.barplot(x=lang_names, y=lang_ranks, palette="viridis")
    plt.title("📊 Challenges per Language")
    plt.xlabel("Language")
    plt.ylabel("Rank (lower is better)")
    plt.xticks(rotation=45)
    plt.savefig(os.path.join(OUTPUT_DIR, "codewars_barchart.svg"), bbox_inches="tight")
    plt.close()

    print("✅ Bar chart generated!")

if __name__ == "__main__":
    stats = fetch_codewars_stats()
    if stats:
        save_csv(stats)
        generate_graphs()
        generate_bar_chart(stats)

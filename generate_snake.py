import numpy as np
import matplotlib.pyplot as plt
import imageio
import os

# Настройки змейки
snake_length = 5  # Начальная длина
frames = 30  # Количество кадров
size = 10  # Размер сегмента
canvas_size = (600, 300)

# Создание папки для вывода
output_dir = "dist"
os.makedirs(output_dir, exist_ok=True)

# Цвета по сезонам
season_colors = {
    "winter": ("#ffffff", "#cce7ff"),
    "spring": ("#00ff99", "#99ff99"),
    "summer": ("#ffcc00", "#ff9933"),
    "autumn": ("#ff6600", "#cc4400"),
}

# Определение текущего сезона
import datetime
month = datetime.datetime.now().month

if month in [12, 1, 2]:
    season = "winter"
elif month in [3, 4, 5]:
    season = "spring"
elif month in [6, 7, 8]:
    season = "summer"
else:
    season = "autumn"

snake_color, background_color = season_colors[season]

# Генерация анимации
images = []
snake = [(50, 150)]  # Начальная позиция змейки
direction = (size, 0)
food = (300, 150)  # Стартовая позиция еды

for i in range(frames):
    # Двигаем голову
    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    snake.insert(0, new_head)

    # Если змейка съела точку — увеличиваем
    if new_head == food:
        food = (np.random.randint(0, canvas_size[0] // size) * size,
                np.random.randint(0, canvas_size[1] // size) * size)
    else:
        snake.pop()

    # Рисуем кадр
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.set_xlim(0, canvas_size[0])
    ax.set_ylim(0, canvas_size[1])
    ax.set_facecolor(background_color)

    # Рисуем змейку
    for segment in snake:
        ax.add_patch(plt.Rectangle(segment, size, size, color=snake_color))

    # Рисуем еду
    ax.add_patch(plt.Rectangle(food, size, size, color="red"))

    plt.axis("off")
    fig.canvas.draw()
    images.append(np.array(fig.canvas.renderer.buffer_rgba()))
    plt.close()

# Сохраняем GIF-анимацию
imageio.mimsave(f"{output_dir}/snake.gif", images, duration=0.1)

# Сохраняем SVG
fig, ax = plt.subplots(figsize=(6, 3))
ax.set_xlim(0, canvas_size[0])
ax.set_ylim(0, canvas_size[1])
ax.set_facecolor(background_color)

for segment in snake:
    ax.add_patch(plt.Rectangle(segment, size, size, color=snake_color))

ax.add_patch(plt.Rectangle(food, size, size, color="red"))

plt.axis("off")
fig.savefig(f"{output_dir}/github-snake.svg", format="svg")
plt.close()

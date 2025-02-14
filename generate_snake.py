import os
import numpy as np
import matplotlib.pyplot as plt
import imageio

# Убеждаемся, что папка dist существует и у неё есть права
output_dir = "dist"
try:
    os.makedirs(output_dir, exist_ok=True)
    os.chmod(output_dir, 0o777)  # Даём полные права на запись
    print(f"✅ Папка '{output_dir}' успешно создана.")
except Exception as e:
    print(f"❌ Ошибка при создании '{output_dir}': {e}")
    exit(1)

# Проверяем, реально ли существует папка
if not os.path.exists(output_dir):
    print("❌ Папка 'dist/' не была создана! Скрипт остановлен.")
    exit(1)

# Генерация SVG и GIF
snake_length = 5
frames = 30
size = 10
canvas_size = (600, 300)

images = []
snake = [(50, 150)]
direction = (size, 0)
food = (300, 150)

for i in range(frames):
    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    snake.insert(0, new_head)

    if new_head == food:
        food = (np.random.randint(0, canvas_size[0] // size) * size,
                np.random.randint(0, canvas_size[1] // size) * size)
    else:
        snake.pop()

    fig, ax = plt.subplots(figsize=(6, 3))
    ax.set_xlim(0, canvas_size[0])
    ax.set_ylim(0, canvas_size[1])
    ax.set_facecolor("#1e1e1e")

    for segment in snake:
        ax.add_patch(plt.Rectangle(segment, size, size, color="lime"))

    ax.add_patch(plt.Rectangle(food, size, size, color="red"))

    plt.axis("off")
    fig.canvas.draw()
    images.append(np.array(fig.canvas.renderer.buffer_rgba()))
    plt.close()

# Сохраняем GIF
gif_path = os.path.join(output_dir, "snake.gif")
try:
    imageio.mimsave(gif_path, images, duration=0.1)
    print(f"✅ GIF сохранён: {gif_path}")
except Exception as e:
    print(f"❌ Ошибка сохранения GIF: {e}")

# Сохраняем SVG
svg_path = os.path.join(output_dir, "github-snake.svg")
try:
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.set_xlim(0, canvas_size[0])
    ax.set_ylim(0, canvas_size[1])
    ax.set_facecolor("#1e1e1e")

    for segment in snake:
        ax.add_patch(plt.Rectangle(segment, size, size, color="lime"))

    ax.add_patch(plt.Rectangle(food, size, size, color="red"))

    plt.axis("off")
    fig.savefig(svg_path, format="svg")
    plt.close()
    print(f"✅ SVG сохранён: {svg_path}")
except Exception as e:
    print(f"❌ Ошибка сохранения SVG: {e}")

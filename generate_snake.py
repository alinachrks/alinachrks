import os
import numpy as np
import matplotlib.pyplot as plt
import imageio

# Создаём папку "dist", если её нет
output_dir = "dist"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Параметры змейки
snake_length = 5  # Начальная длина
frames = 30  # Количество кадров
size = 10  # Размер сегмента
canvas_size = (600, 300)

# Генерация анимации змейки
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

    # Рисуем кадр
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

# Сохраняем GIF-анимацию
imageio.mimsave(f"{output_dir}/snake.gif", images, duration=0.1)

# Сохраняем SVG
fig, ax = plt.subplots(figsize=(6, 3))
ax.set_xlim(0, canvas_size[0])
ax.set_ylim(0, canvas_size[1])
ax.set_facecolor("#1e1e1e")

for segment in snake:
    ax.add_patch(plt.Rectangle(segment, size, size, color="lime"))

ax.add_patch(plt.Rectangle(food, size, size, color="red"))

plt.axis("off")
fig.savefig(f"{output_dir}/github-snake.svg", format="svg")
plt.close()

import random


def estimate_pi(num_samples):
    inside_circle = 0

    for _ in range(num_samples):
        x = random.uniform(-1, 1)  # Генерация случайной координаты X в диапазоне [-1, 1]
        y = random.uniform(-1, 1)  # Генерация случайной координаты Y в диапазоне [-1, 1]

        if x ** 2 + y ** 2 <= 1:  # Проверяем, находится ли точка внутри единичного круга
            inside_circle += 1

    pi_estimate = 4 * inside_circle / num_samples
    return pi_estimate


# Оцениваем число Пи с использованием 10000000 образцов
pi_approx = estimate_pi(10000000)
print(f'Приблизительное значение числа Пи: {pi_approx}')
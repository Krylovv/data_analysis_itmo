import random
import matplotlib.pyplot as plt
from scipy.stats import norm
import numpy as np


def roll_dices(num_dices, num_rolls):
    # Генерация сумм нескольких кубиков
    results = []
    for _ in range(num_rolls):
        result = sum(random.randint(1, 6) for _ in range(num_dices))
        results.append(result)

    return results


def plot_histogram_with_normal_distribution(results, num_dices, num_rolls):
    # Определение минимального и максимального значения суммы
    min_sum = num_dices
    max_sum = num_dices * 6

    # Построение гистограммы
    plt.figure(figsize=(8, 6))  # Устанавливаем размер фигуры
    plt.hist(results, bins=max_sum - min_sum + 1, range=(min_sum - 0.5, max_sum + 0.5), edgecolor='black', align='mid',
             density=True)

    # Вычисление среднего и стандартного отклонения
    mean = sum(results) / len(results)
    std_dev = (sum((x - mean) ** 2 for x in results) / len(results)) ** 0.5

    # Построение нормального распределения
    x = np.linspace(min_sum, max_sum, 100)
    normal_curve = norm.pdf(x, loc=mean, scale=std_dev)
    plt.plot(x, normal_curve, color='red', linewidth=2, label='Нормальное распределение')

    plt.xlabel('Сумма бросков')
    plt.ylabel('Частота')
    plt.title(f'Гистограмма результатов {num_rolls} бросков {num_dices} кубиков')
    plt.legend()
    plt.grid(True)  # Добавляем сетку для удобства чтения
    plt.show()


if __name__ == "__main__":
    # Ввод количества кубиков и количества бросков
    num_dices = int(input("Введите количество кубиков: "))
    num_rolls = int(input("Введите количество бросков: "))

    # Выполнение эксперимента и построение гистограммы
    results = roll_dices(num_dices, num_rolls)
    plot_histogram_with_normal_distribution(results, num_dices, num_rolls)
import numpy as np
import matplotlib.pyplot as plt

# Генерация случайных данных
np.random.seed(42)
x = np.linspace(0, 10, 100)
y = 2 * x + 3 + np.random.normal(size=len(x))

# Вычисление математического ожидания и среднеквадратичного отклонения
mean_x = np.mean(x)
mean_y = np.mean(y)
std_deviation_x = np.std(x)
std_deviation_y = np.std(y)
print(f"Математическое ожидание X: {mean_x:.4f}")
print(f"Среднеквадратичное отклонение X: {std_deviation_x:.4f}")
print(f"Математическое ожидание Y: {mean_y:.4f}")
print(f"Среднеквадратичное отклонение Y: {std_deviation_y:.4f}")

# Метод наименьших квадратов для построения линейной функции
def least_squares(x, y):
    # Коэффициенты a и b для уравнения прямой вида y = ax + b
    a = (len(x) * np.sum(x * y) - np.sum(x) * np.sum(y)) / (len(x) * np.sum(x**2) - np.sum(x)**2)
    b = (np.sum(y) - a * np.sum(x)) / len(x)
    return a, b


a, b = least_squares(x, y)
print(f"Коэффициент a: {a:.4f}, коэффициент b: {b:.4f}")

# Построение графика исходных данных и аппроксимирующей линии
plt.scatter(x, y, label='Исходные данные')
plt.plot(x, a * x + b, color='red', label='Аппроксимация методом наименьших квадратов')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.show()
import pandas as pd
import matplotlib.pyplot as plt

# Загрузка данных
# df = pd.read_csv('lab5_data.csv', parse_dates=['Дата'])
df = pd.read_csv('lab5_data_2.csv', parse_dates=['Дата'])

# Проверка наличия пропущенных значений
print("Пропуски в данных:")
print(df.isnull().sum())

# Заполнение пропусков средними значениями по колонке 'Сумма'
if df['Сумма'].isna().any():
    df['Сумма'] = df['Сумма'].fillna(df['Сумма'].mean())

# Расчет математического ожидания
mean_sum = df['Сумма'].mean()
print(f"Математическое ожидание суммы продаж: {mean_sum:.2f}")


# Расчет дисперсии и стандартного отклонения
variance = df['Сумма'].var()
std_dev = df['Сумма'].std()
print(f"Дисперсия суммы продаж: {variance:.2f}")
print(f"Стандартное отклонение суммы продаж: {std_dev:.2f}")


# Анализ по категориям
categories = df['Категория'].unique()
for category in categories:
    cat_df = df.query("Категория == @category")

    # Математическое ожидание
    mean_cat = cat_df['Сумма'].mean()
    print(f"\nМатематическое ожидание для категории '{category}': {mean_cat:.2f}")

    # Дисперсия и стандартное отклонение
    variance_cat = cat_df['Сумма'].var()
    std_dev_cat = cat_df['Сумма'].std()
    print(f"Дисперсия для категории '{category}': {variance_cat:.2f}")
    print(f"Стандартное отклонение для категории '{category}': {std_dev_cat:.2f}")

# Визуализация данных
plt.figure(figsize=(10, 6))

# Гистограмма распределения сумм продаж
# plt.subplot(211)
plt.hist(df['Сумма'], bins=20, edgecolor='black')
plt.title('Распределение суммы продаж')
plt.xlabel('Сумма')
plt.ylabel('Частота')

# Боксплот для сравнения категорий
# plt.subplot(212)
# plt.boxplot([df.query("Категория == @cat")['Сумма'] for cat in categories], labels=categories)
# plt.title('Боксплот для различных категорий')
# plt.xlabel('Категория')
# plt.ylabel('Сумма')

plt.tight_layout()
plt.show()

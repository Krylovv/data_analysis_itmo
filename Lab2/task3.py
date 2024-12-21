import yfinance
import numpy as np
from scipy.stats import mstats
import matplotlib.pyplot as plt

# Указываем тикеры и период загрузки данных
tickers = ["V", "MA"]
start_date = '2023-01-01'
end_date = '2023-12-31'

# Загружаем данные
data = yfinance.download(tickers, start=start_date, end=end_date)
# Используем столбцы Close для расчета корреляции
visa_close = data['Close']['V']
mastercard_close = data['Close']['MA']

correlation = np.corrcoef(visa_close, mastercard_close)[0][1]
print(f"Коэффициент корреляции Пирсона: {correlation:.4f}")


def remove_random_data(dataframe, n=10):
    """
    Функция заменяет случайным образом n значений в DataFrame на NaN.
    """
    index_to_replace = np.random.choice(dataframe.index, size=n, replace=False)
    dataframe.loc[index_to_replace] = np.nan
    return dataframe


# Удаляем случайно 10 значений из каждого ряда
removed_visa_close = remove_random_data(visa_close.copy())
removed_mastercard_close = remove_random_data(mastercard_close.copy())


def winsorize(data):
    """
    Выполняет винзоризацию данных.
    """

    # Заполняем пропущенные значения ближайшими допустимыми значениями
    series_filled = data.bfill()
    return series_filled


winsorized_visa_close = winsorize(removed_visa_close)
winsorized_mastercard_close = winsorize(removed_mastercard_close)


def linear_interpolation(data):
    """
    Восстанавливает пропущенные значения методом линейной интерполяции.
    """
    return data.interpolate(method='linear')

interpolated_visa_close = linear_interpolation(removed_visa_close)
interpolated_mastercard_close = linear_interpolation(removed_mastercard_close)


def correlation_restore(x, y, x_missing):
    """
    Восстанавливает пропущенные значения в X на основе корреляции с Y.
    """
    idx = ~x_missing.isna()  # Проверка на NaN
    slope, intercept = np.polyfit(y[idx], x[idx], 1)
    restored_x = x_missing.copy()
    restored_x[~idx] = slope * y[~idx] + intercept  # Используем индексы без NaN

    return restored_x


restored_visa_close = correlation_restore(visa_close, mastercard_close, removed_visa_close)
restored_mastercard_close = correlation_restore(mastercard_close, visa_close, removed_mastercard_close)

# Графики
plt.figure(figsize=(15, 8))

# # Винзоризация Visa
# plt.subplot(221)
# plt.plot(visa_close, label="Оригинал")
# plt.plot(winsorized_visa_close, label="Винзоризация")
# plt.legend()
# plt.title("Visa - Винзоризация")
#
# # Винзоризация MasterCard
# plt.subplot(222)
# plt.plot(mastercard_close, label="Оригинал")
# plt.plot(winsorized_mastercard_close, label="Винзоризация")
# plt.legend()
# plt.title("MasterCard - Винзоризация")

# plt.subplot(221)
# plt.plot(visa_close, label="Оригинал")
# plt.plot(interpolated_visa_close, label="Интерполяция")
# plt.legend()
# plt.title("Visa - Интерполяция")
#
# plt.subplot(222)
# plt.plot(mastercard_close, label="Оригинал")
# plt.plot(interpolated_mastercard_close, label="Интерполяция")
# plt.legend()
# plt.title("MasterCard - Интерполяция")

#
# plt.subplot(221)
# plt.plot(visa_close, label="Оригинал")
# plt.plot(restored_visa_close, label="Корреляционное восстановление")
# plt.legend()
# plt.title("Visa - Корреляционное восстановление")
#
# plt.subplot(222)
# plt.plot(mastercard_close, label="Оригинал")
# plt.plot(restored_mastercard_close, label="Корреляционное восстановление")
# plt.legend()
# plt.title("Mastercard - Корреляционное восстановление")
#
# plt.tight_layout()
# plt.show()

visa_winsor_dif = visa_close - winsorized_visa_close
master_winsor_dif = mastercard_close - winsorized_mastercard_close
visa_interpol_dif = visa_close - interpolated_visa_close
master_interpol_dif = mastercard_close - interpolated_mastercard_close
visa_corr_dif = visa_close - restored_visa_close
master_corr_dif = mastercard_close - restored_mastercard_close

# Находим среднее арифметическое разностей
visa_winsor_average_difference = visa_winsor_dif.mean()
master_winsor_average_difference = master_winsor_dif.mean()
visa_interpol_average_difference = visa_interpol_dif.mean()
master_interpol_average_difference = master_interpol_dif.mean()
visa_corr_average_difference = visa_corr_dif.mean()
master_corr_average_difference = master_corr_dif.mean()

average_winsor = (abs(visa_winsor_average_difference) + abs(master_winsor_average_difference)) / 2
average_interpol = (abs(visa_interpol_average_difference) + abs(master_interpol_average_difference)) / 2
average_corr = (abs(visa_corr_average_difference) + abs(master_corr_average_difference)) / 2

print(f'Средняя разница элементов при восстановлении винзорированием: {average_winsor}')
print(f'Средняя разница элементов при восстановлении интерполяцией: {average_interpol}')
print(f'Средняя разница элементов при корреляционном восстановлении: {average_corr}')

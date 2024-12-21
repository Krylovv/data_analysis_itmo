import yfinance as yf
import numpy as np

# Список тикеров
tickers = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'TSLA']

# Загрузка данных
data = yf.download(tickers, start='2023-01-01', end='2023-12-31')

def simple_moving_average(data, window):
    return data.rolling(window=window, min_periods=3).mean()

# Применение простого скользящего среднего к данным
sma_data = {}
for ticker in tickers:
    sma_data[ticker] = simple_moving_average(data['Close'][ticker], 20)

def weighted_moving_average(data, window):
    weights = list(range(1, window + 1))
    wma = data.rolling(window=window).apply(lambda x: np.dot(x, weights)/sum(weights), raw=True)
    return wma

# Применение взвешенного скользящего среднего к данным
wma_data = {}
for ticker in tickers:
    wma_data[ticker] = weighted_moving_average(data['Close'][ticker], 10)


def exponential_smoothing(data, alpha):
    es = data.ewm(alpha=alpha, adjust=False).mean()
    return es

# Применение экспоненциального сглаживания к данным
es_data = {}
for ticker in tickers:
    es_data[ticker] = exponential_smoothing(data['Close'][ticker], 0.1)

import matplotlib.pyplot as plt

plt.figure(figsize=(15, 10))

for i, ticker in enumerate(tickers):
    ax = plt.subplot(len(tickers), 1, i + 1)

    # Оригинальные данные
    ax.plot(data['Close'][ticker].index, data['Close'][ticker], label='Оригинальные данные')

    # Простое скользящее среднее
    ax.plot(sma_data[ticker].index, sma_data[ticker], label='Простое скользящее среднее')

    # Взвешенное скользящее среднее
    ax.plot(wma_data[ticker].index, wma_data[ticker], label='Взвешенное скользящее среднее')

    # Экспоненциальное сглаживание
    ax.plot(es_data[ticker].index, es_data[ticker], label='Экспоненциальное сглаживание')

    ax.set_title(f'{ticker}')
    ax.legend()

plt.tight_layout()
plt.show()

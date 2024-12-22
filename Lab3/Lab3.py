import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import squarify
from random import choices, randint
import plotly.express as px
import plotly.graph_objects as go

# Генерация случайных данных
np.random.seed(42)

# Возможные значения
products = ['Продукт A', 'Продукт B', 'Продукт C', 'Продукт D']
regions = ['Регион 1', 'Регион 2', 'Регион 3', 'Регион 4', 'Регион 5']
months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
          'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

# Создание DataFrame
data = []
for product in products:
    for region in regions:
        for month in months:
            quantity_sold = randint(50, 200)
            revenue = quantity_sold * np.random.uniform(100, 500)
            data.append({
                'Product': product,
                'Region': region,
                'Month': month,
                'Quantity_Sold': quantity_sold,
                'Revenue': revenue
            })

df = pd.DataFrame(data)

# 1. Диаграмма столбцов общего количества продаж для каждого продукта
product_sales = df.groupby('Product')['Quantity_Sold'].sum().reset_index()

plt.figure(figsize=(10, 6))
plt.bar(product_sales['Product'], product_sales['Quantity_Sold'])
plt.xlabel('Название продукта')
plt.ylabel('Общее количество продаж')
plt.title('Количество продаж по продуктам')
plt.show()

# 2. Столбчатая диаграмма суммарного дохода по регионам
region_revenue = df.groupby('Region')['Revenue'].sum().reset_index()

plt.figure(figsize=(10, 6))
plt.bar(region_revenue['Region'], region_revenue['Revenue'])
plt.xlabel('Регионы')
plt.ylabel('Суммарный доход')
plt.title('Доход от продаж по регионам')
plt.show()

# 3. Круговая диаграмма процентного соотношения дохода по месяцам
month_revenue = df.groupby('Month')['Revenue'].sum().reset_index()
total_revenue = month_revenue['Revenue'].sum()
month_revenue['Percentage'] = month_revenue['Revenue'] / total_revenue * 100

# Устанавливаем порядок месяцев
month_order = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
month_revenue['Month'] = pd.Categorical(month_revenue['Month'], categories=month_order, ordered=True)
month_revenue.sort_values(by='Month', inplace=True)

plt.figure(figsize=(10, 6))
plt.pie(month_revenue['Percentage'], labels=month_revenue['Month'],
       autopct='%1.1f%%', startangle=140)
plt.axis('equal')
plt.title('Процентное соотношение дохода по месяцам')
plt.show()

# 4. Scatter plot для связи между количеством продаж и доходом
plt.figure(figsize=(10, 6))
plt.scatter(df['Quantity_Sold'], df['Revenue'])
plt.xlabel('Количество продаж')
plt.ylabel('Доход')
plt.title('Зависимость дохода от количества продаж')
plt.show()

# 5. Линейный график динамики дохода по месяцам
plt.figure(figsize=(10, 6))
plt.plot(months, month_revenue['Revenue'])
plt.xlabel('Месяцы')
plt.ylabel('Доход')
plt.title('Динамика дохода по месяцам')
plt.show()

# 6. Гистограмма распределения количества продаж
bins = [0, 50, 100, 150, 200]
labels = ['0-50', '51-100', '101-150', '151-200']

quantity_bins = pd.cut(df['Quantity_Sold'], bins=bins, labels=labels)
quantity_counts = quantity_bins.value_counts(sort=False).sort_index()

plt.figure(figsize=(10, 6))
plt.bar(quantity_counts.index, quantity_counts.values)
plt.xlabel('Диапазон количества продаж')
plt.ylabel('Частота')
plt.title('Распределение количества продаж по диапазонам')
plt.show()

# 7. Heatmap для визуализации взаимосвязи между регионами и количеством продаж
sales_by_region = df.pivot_table(index='Region', columns='Product', values='Quantity_Sold', aggfunc=np.sum)

plt.figure(figsize=(10, 6))
sns.heatmap(sales_by_region, annot=True, fmt="d")
plt.title('Тепловая карта количества продаж по регионам и продуктам')
plt.show()

# 8. Box plot для визуализации распределения и выбросов по доходу от продаж
plt.figure(figsize=(10, 6))
plt.boxplot(df['Revenue'], vert=False)
plt.xlabel('Доход')
plt.title('Box plot распределения дохода от продаж')
plt.grid(True)
plt.show()

# 9. Treemap для визуализации доли дохода от продаж в каждом регионе
region_revenue_dict = dict(zip(region_revenue['Region'], region_revenue['Revenue']))

plt.figure(figsize=(10, 6))
squarify.plot(sizes=list(region_revenue_dict.values()), label=list(region_revenue_dict.keys()),
              alpha=.7, color=sns.color_palette('Spectral', len(list(region_revenue_dict.values()))),
              pad=1, text_kwargs=dict(fontsize=12))
plt.title('Treemap доли дохода от продаж по регионам')
plt.axis('off')
plt.show()

# 10. Violin plot для визуализации распределения дохода по продуктам
plt.figure(figsize=(10, 6))
sns.violinplot(x='Product', y='Revenue', data=df)
plt.xlabel('Продукты')
plt.ylabel('Доход')
plt.title('Violin plot распределения дохода по продуктам')
plt.grid(True)
plt.show()

# 11. Stacked bar plot для визуализации соотношения дохода от продаж для разных продуктов в каждом регионе
revenue_by_product_and_region = df.pivot_table(index='Region', columns='Product', values='Revenue', aggfunc=np.sum)

plt.figure(figsize=(10, 6))
revenue_by_product_and_region.plot(kind='bar', stacked=True)
plt.xlabel('Регионы')
plt.ylabel('Доход')
plt.title('Stacked bar plot дохода по продуктам и регионам')
plt.legend(title='Продукты')
plt.show()

# 18. Анимация динамики изменений продаж и дохода
animation_df = df.groupby(['Month', 'Product'])[['Quantity_Sold', 'Revenue']].sum().reset_index()
fig = px.line(animation_df, x='Month', y='Quantity_Sold', color='Product', animation_frame='Product',
              range_y=[0, animation_df['Quantity_Sold'].max()], title='Динамика изменения количества продаж по продуктам')

fig.update_layout(
    xaxis_title="Месяцы",
    yaxis_title="Количество продаж",
    legend_title="Продукты",
    updatemenus=[
        {
            "buttons": [
                {"args": [None, {"frame": {"duration": 3000}}], "label": "Play", "method": "animate"},
                {"args": [[None], {"frame": {"duration": 0, "redraw": False}},
                          {"fromcurrent": True, "transition": {"duration": 300, "easing": "quadratic-in-out"}}],
                 "label": "Pause",
                 "method": "animate"}
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 87},
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": 0,
            "yanchor": "top"
        }
    ]
)
fig.show()

# 19. Сложный график с использованием нескольких слоев данных
fig = go.Figure()

# Добавление столбцовой диаграммы для количества продаж
fig.add_trace(go.Bar(name='Количество продаж', x=product_sales['Product'], y=product_sales['Quantity_Sold']))

# Добавление линии для дохода
fig.add_trace(go.Scatter(name='Доход', x=product_sales['Product'], y=product_sales['Quantity_Sold']*250, mode='lines+markers'))

# Настройки графика
fig.update_layout(barmode='group', title='Сравнение количества продаж и дохода по продуктам')

# Показ графика
fig.show()

import netCDF4 as nc
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np

# Load the NetCDF file
file_path = 'data/adaptor.mars.internal-1718484777.0788732-20565-7-3cd808eb-9068-4011-9ab6-12596691967d.nc'
dataset = nc.Dataset(file_path)

# Extract the necessary data
temperature = dataset.variables['t2m'][:]  # Adjust the variable name as needed
lons = dataset.variables['longitude'][:]
lats = dataset.variables['latitude'][:]

# Convert temperature from Kelvin to Celsius if needed
temperature = temperature - 273.15

# Create the plot
plt.figure()
ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines()
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.add_feature(cfeature.LAND, edgecolor='black')
ax.add_feature(cfeature.LAKES, edgecolor='black')
ax.add_feature(cfeature.RIVERS)

# Create a contour plot
contour = plt.contourf(lons, lats, temperature[0, :, :], cmap='coolwarm', transform=ccrs.PlateCarree())

# Add a colorbar
cbar = plt.colorbar(contour, orientation='vertical', pad=0.05, aspect=50)
cbar.set_label('Temperature (°C)')

# Add title
plt.title('2 Metre Temperature')

# Show the plot
plt.show()

# import plotly.graph_objects as go
# from netCDF4 import Dataset
#
# # Загрузка данных из файла NetCDF
# data = Dataset('data/Fields/temperature_2m_ERA5_08_2019.nc')
#
# # Получение массива температур
# temperature_data = data.variables['t2m'][:]
#
# # Создание карты мира
# fig = go.Figure()
#
# # Добавление температурных данных на карту мира
# fig.add_trace(go.Choropleth(
#     locations=['USA', 'CAN', 'GBR', 'IND', 'CHN'],  # Список стран или регионов
#     locationmode='country names',
#     z=temperature_data[0,:,:],  # Выбираем температурные данные для первого временного шага (индекс 0)
#     colorscale='Viridis',  # Цветовая шкала
#     colorbar_title='Temperature (K)',  # Название цветовой шкалы
# ))
# fig.add_trace(go.Choropleth(
#     locations=['USA', 'CAN', 'GBR', 'IND', 'CHN'],  # Список стран или регионов
#     locationmode='country names',
#     z=temperature_data[0,:,:],  # Выбираем температурные данные для первого временного шага (индекс 0)
#     colorscale='Viridis',  # Цветовая шкала
#     colorbar_title='Temperature (K)',  # Название цветовой шкалы
# ))
# # Настройка макета карты
# fig.update_layout(
#     title_text='World Temperature',
#     geo=dict(
#         showcoastlines=True,
#         projection_type='equirectangular'
#     )
# )
#
# # Отображение карты
# fig.show()
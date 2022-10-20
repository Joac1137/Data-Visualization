import geopandas as gpd
import pandas as pd

file = "small_umbrella_terms_crimes"

url = 'https://raw.githubusercontent.com/magnuslarsen/geoJSON-Danish-municipalities/master/municipalities/municipalities.geojson'
gdf = gpd.read_file(url)
gdf = gdf[['label_dk','geometry']]
gdf.loc[gdf.label_dk == 'Århus', 'label_dk'] = "Aarhus"
gdf.loc[gdf.label_dk == 'Brønderslev-Dronninglund', 'label_dk'] = "Brønderslev"
gdf.loc[gdf.label_dk == 'Vesthimmerland', 'label_dk'] = "Vesthimmerlands"
gdf = gdf.dissolve(by='label_dk')




df = pd.read_csv("data/" + file + ".csv", encoding="utf_8")
df = df.rename(columns={'område': 'label_dk', "overtrædelsens art": "offence"})
df = df.astype({'Anmeldte forbrydelser': 'int32'})
#df['tid'] = df['tid'].apply(lambda x : x[:-2])
#df = df.groupby(['tid','offence','label_dk'])['Anmeldte forbrydelser'].sum().reset_index()

big_fuck_df = gdf.merge(df, how='left', on='label_dk')
big_fuck_df.to_file("data_with_geo/" + file + "_quarters.geojson", driver='GeoJSON')
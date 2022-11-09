import geopandas as gpd
import pandas as pd
import valuecodes

file = "umbrella_terms_crimes"
"""
url = 'https://raw.githubusercontent.com/magnuslarsen/geoJSON-Danish-municipalities/master/municipalities/municipalities.geojson'
gdf = gpd.read_file(url)
print(gdf.columns)
gdf['type'] = "Feature"
gdf = gdf[['label_dk','geometry','type']]
gdf.loc[gdf.label_dk == 'Århus', 'label_dk'] = "Aarhus"
gdf.loc[gdf.label_dk == 'Brønderslev-Dronninglund', 'label_dk'] = "Brønderslev"
gdf.loc[gdf.label_dk == 'Vesthimmerland', 'label_dk'] = "Vesthimmerlands"
gdf = gdf.dissolve(by='label_dk')
gdf.to_file("data_with_geo/" + "geometry" + ".geojson", driver='GeoJSON')
"""

df = pd.read_csv("data/" + file + ".csv", encoding="utf_8")
df = df.rename(columns={'område': 'label_dk', "overtrædelsens art": "offence"})
df = df.astype({'Anmeldte forbrydelser': 'int32'})

#df['tid'] = df['tid'].apply(lambda x : x[:-2])
#df = df.groupby(['tid','offence','label_dk'])['Anmeldte forbrydelser'].sum().reset_index()
#file = file + "_years"

pop_df = pd.read_csv("data/populations.csv", encoding="utf_8")
pop_df = pop_df.rename(columns={'område': 'label_dk','Folketal den 1. i kvartalet':'population'})
df = df.merge(pop_df, how="inner", on=['label_dk', 'tid'])
file = file + "_pop"


kommune_to_region ={}
for k in valuecodes.region_to_kommune:
    for v in valuecodes.region_to_kommune[k]:
        kommune_to_region[v] = k
print(kommune_to_region)

df['region_dk'] = df.apply(lambda row: kommune_to_region[row['label_dk']], axis=1)
file = file + "_regional"


df.to_csv("data/"+ file + ".csv")

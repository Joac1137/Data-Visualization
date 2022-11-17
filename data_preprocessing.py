import geopandas as gpd
import pandas as pd
import valuecodes
import repository as repo


def GetMuncipaltyGeoJson():
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

def PreprocessData(fileName = "umbrella_data_prepared",fromFile = False):
    df = pd.DataFrame
    if fromFile:
        df = pd.read_csv("data/umbrella_terms_crimes.csv", encoding="utf_8")
    else:
        df = repo.CreateUmbrellaCrimeCSV()
    df = df.rename(columns={'område': 'label_dk', "overtrædelsens art": "offence"})
    df = df.astype({'Anmeldte forbrydelser': 'int32'})
    for i in valuecodes.Crime_Translation.keys():
        df.loc[df['offence'] == i, 'offence'] = valuecodes.Crime_Translation[i]
    #df['tid'] = df['tid'].apply(lambda x : x[:-2])
    #df = df.groupby(['tid','offence','label_dk'])['Anmeldte forbrydelser'].sum().reset_index()
    #file = file + "_years"
    pop_df = pd.read_csv("data/populations.csv", encoding="utf_8")
    pop_df = pop_df.rename(columns={'område': 'label_dk','Folketal den 1. i kvartalet':'population'})
    df = df.merge(pop_df, how="inner", on=['label_dk', 'tid'])
    df['population_scaled'] = df['population'].div(100000)
    df['forbrydelser_pr_100k_indbygger'] = df['Anmeldte forbrydelser']/df['population_scaled']
    df['tid'] = df['tid'].str.replace('K','-Q')
    df['tid'] = pd.to_datetime(df['tid'])
    df.to_csv("data/"+ fileName + ".csv")



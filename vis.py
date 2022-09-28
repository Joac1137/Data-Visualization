import geopandas as gpd
import altair as alt
import requests
import pandas as pd

# Example of requests
# response = requests.get("https://api.statbank.dk/v1/data/STRAF10/JSONSTAT?OVERTR%C3%86D=1289%2C3820&Tid=2021K1%2C2021K2%2C2021K3%2C2021K4%2C2022K1%2C2022K2")
# print(response.json())

df = pd.read_csv("2022928135943390963562STRAF1150490172666.csv")
df = df.rename(columns={' .1' : 'label_dk'})
df = df.drop(' ', axis=1)


# load raw url in geodataframe
url = 'https://raw.githubusercontent.com/magnuslarsen/geoJSON-Danish-municipalities/master/municipalities/municipalities.geojson'
gdf = gpd.read_file(url)

# set projection and reproject
gdf.crs = {'init' :'epsg:27700'}
gdf = gdf.to_crs({'init': 'epsg:4326'})

# define inline geojson data object
data_geojson = alt.InlineData(values=gdf.to_json(), format=alt.DataFormat(property='features',type='json')) 

# Merge the df
data = gdf.merge(df, how='left', on='label_dk')


# chart object
char1 = alt.Chart(data).mark_geoshape(
).encode(
    color=alt.Color(
            "2022K1:Q",
            scale=alt.Scale(scheme='viridis')
            )
).properties(
    width=500,
    height=300
)

char2 = alt.Chart(data).mark_geoshape(
).encode(
    color=alt.Color(
            "2022K1:O",
            scale=alt.Scale(scheme='viridis')
            )
).properties(
    width=500,
    height=300
)

chart = alt.concat(char1, char2)
chart.show()



# # chart object
# alt.Chart(data_geojson).mark_geoshape(
# ).encode(
#     color='2022K1:Q'
# ).transform_lookup(
#     lookup='label_dk',
#     from_=alt.LookupData(data=df, key='label_dk', fields=['2022K1'])
# ).show()

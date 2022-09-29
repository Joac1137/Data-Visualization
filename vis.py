import geopandas as gpd
import altair as alt
import requests
import pandas as pd
import io

# Example of requests
response = requests.get("https://api.statbank.dk/v1/data/STRAF11/JSONSTAT?OMR%C3%85DE=*&OVERTR%C3%86D=1&Tid=*").content
print(response)
df = pd.read_json(io.StringIO(response.decode('utf-8')))

#print(response.json())
#df = pd.read_json(response.json())
#df = pd.read_csv("2022928135943390963562STRAF1150490172666.csv")
df = df.rename(columns={' .1' : 'label_dk'})
df = df.drop(' ', axis=1)


# load raw url in geodataframe
url = 'https://raw.githubusercontent.com/magnuslarsen/geoJSON-Danish-municipalities/master/municipalities/municipalities.geojson'
gdf = gpd.read_file(url)

# Merge the data frames
data = gdf.merge(df, how='left', on='label_dk')
#data = data.fillna(0)

# define inline geojson data object
data_geojson = alt.InlineData(values=gdf.to_json(), format=alt.DataFormat(property='features',type='json')) 


# chart object
char1 = alt.Chart(data).mark_geoshape(
).encode(
    color=alt.Color(
            "2007K1:Q",
            scale=alt.Scale(scheme='viridis')
            )
).properties(
    width=500,
    height=300
)

char2 = alt.Chart(data).mark_geoshape(
).encode(
    color=alt.value("#FFAA00")
).properties(
    width=500,
    height=300
)

chart = alt.concat(char1, char2)
#chart = char1 + char2
chart.show()



# # chart object
# alt.Chart(data_geojson).mark_geoshape(
# ).encode(
#     color='2022K1:Q'
# ).transform_lookup(
#     lookup='label_dk',
#     from_=alt.LookupData(data=df, key='label_dk', fields=['2022K1'])
# ).show()

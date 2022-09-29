import geopandas as gpd
import altair as alt
import pandas as pd


# df = pd.read_csv("2022928135943390963562STRAF1150490172666.csv")

df = pd.read_csv("crime_data.csv", encoding="iso-8859-1")
df = df.rename(columns={' .1' : 'label_dk'})
df = df.drop(' ', axis=1)


# load raw url in geodataframe
url = 'https://raw.githubusercontent.com/magnuslarsen/geoJSON-Danish-municipalities/master/municipalities/municipalities.geojson'
gdf = gpd.read_file(url)

# Merge the data frames
data = gdf.merge(df, how='left', on='label_dk')
data = data.fillna(0)

# define inline geojson data object
data_geojson = alt.InlineData(values=gdf.to_json(), format=alt.DataFormat(property='features',type='json')) 

columns = df.columns.to_list()[1:]

time_dropdown = alt.binding_select(options=columns, name='Time')
time_selection = alt.selection_single(fields=['Time'], bind=time_dropdown)
# single = alt.selection_single()

# color=alt.condition(
#         single, 
#         alt.Color(
#             "2007K1:Q",
#             scale=alt.Scale(
#                 scheme='viridis')
#         ), 
#         alt.value('lightgray'))

# chart object
char = alt.Chart(data).transform_fold(
    columns,
    as_=['Time', 'value']
).transform_filter(
    time_selection  
).mark_geoshape().encode(
    color='value:Q'
).add_selection(
    time_selection
).properties(
    width=500,
    height=300
)
char.show()

import geopandas as gpd
import altair as alt
import pandas as pd


# df = pd.read_csv("2022928135943390963562STRAF1150490172666.csv")
# df = df.rename(columns={' .1' : 'label_dk'})
# df = df.drop(' ', axis=1)
df = pd.read_csv("crime_data.csv", encoding='utf-8')

print(df)

# # load raw url in geodataframe
# url = 'https://raw.githubusercontent.com/magnuslarsen/geoJSON-Danish-municipalities/master/municipalities/municipalities.geojson'
# gdf = gpd.read_file(url)

# # Merge the data frames
# data = gdf.merge(df, how='left', on='label_dk')
# data = data.fillna(0)

# # define inline geojson data object
# data_geojson = alt.InlineData(values=gdf.to_json(), format=alt.DataFormat(property='features',type='json')) 


# single = alt.selection_single()

# # chart object
# char = alt.Chart(data).mark_geoshape().encode(
#     color=alt.condition(
#         single, 
#         alt.Color(
#             "2007K1:Q",
#             scale=alt.Scale(
#                 scheme='viridis')
#         ), 
#         alt.value('lightgray'))
# ).add_selection(
#     single
# ).properties(
#     width=500,
#     height=300
# )
# char.show()

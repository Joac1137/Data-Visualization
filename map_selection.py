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


height = 600
map_width = 1000
barchart_width = 30


columns = df.columns.to_list()[1:5]

time_dropdown = alt.binding_select(options=columns, name='Time')
time_selection = alt.selection_single(fields=['Time'], bind=time_dropdown)


municipality_selection = alt.selection_single()

# chart object
char = alt.Chart(data).mark_geoshape().encode(
    color='time_value:Q'
).transform_fold(
    columns,
    as_=['Time', 'time_value']
).transform_filter(
    time_selection  
).add_selection(
    time_selection
).add_selection(
    municipality_selection
).encode(
    color=alt.condition(
        municipality_selection, 
        alt.Color(
            "time_value:Q",
            scale=alt.Scale(
                scheme='viridis')
        ), 
        alt.value('lightgray'))
).properties(
    width=map_width,
    height=height
)


hist = alt.Chart(data).mark_bar().encode(
    x='value:N',
    y='time_value:Q'
).transform_filter(
    municipality_selection
).transform_fold(
    columns,
    as_=['Time', 'time_value']
).transform_filter(
    time_selection
).properties(
    width=barchart_width,
    height=height
)

charts = alt.concat(char, hist)

charts.show()

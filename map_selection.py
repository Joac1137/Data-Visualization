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


# chart object
char = alt.Chart(data).mark_geoshape().encode(
    color='value:Q'
).properties(
    width=500,
    height=300
)


columns = df.columns.to_list()[1:]

time_dropdown = alt.binding_select(options=columns, name='Time')
time_selection = alt.selection_single(fields=['Time'], bind=time_dropdown)

char = char.transform_fold(
    columns,
    as_=['Time', 'value']
).transform_filter(
    time_selection  
).add_selection(
    time_selection
)



#municipality = df['label_dk'].tolist()
single = alt.selection_single()

# char = char.add_selection(
#     single
# )



char = char.add_selection(
    single
).encode(
    color=alt.condition(
        single, 
        alt.Color(
            "value:Q",
            scale=alt.Scale(
                scheme='viridis')
        ), 
        alt.value('lightgray'))
)


hist = alt.Chart(data).mark_bar().encode(
    x='value:N',
    y='2007K1:Q'
).transform_filter(
    single
)

charts = alt.concat(char, hist)

charts.show()

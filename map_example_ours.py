import pandas as pd
import altair as alt
import geopandas as gpd
import valuecodes
import matplotlib as plt

alt.data_transformers.enable('default', max_rows=None)

url = 'https://raw.githubusercontent.com/magnuslarsen/geoJSON-Danish-municipalities/master/municipalities/municipalities.geojson'
gdf = gpd.read_file(url)
gdf = gdf[['label_dk','geometry']]
gdf.loc[gdf.label_dk == 'Århus', 'label_dk'] = "Aarhus"
gdf.loc[gdf.label_dk == 'Brønderslev-Dronninglund', 'label_dk'] = "Brønderslev"
gdf.loc[gdf.label_dk == 'Vesthimmerland', 'label_dk'] = "Vesthimmerlands"
gdf = gdf.dissolve(by='label_dk')

df = pd.read_csv("data/mini_crimes.csv", encoding="utf_8")
df = df.rename(columns={'område': 'label_dk', "overtrædelsens art": "offence"})
df = df.astype({'Anmeldte forbrydelser': 'int32'})

big_fuck_df = gdf.merge(df, how='left', on='label_dk')




offence_selection = alt.selection_single(init={'offence':'Voldtægt mv.'})
time_selection = alt.selection_interval(encodings=['x'])
area_selection = alt.selection_single(fields=['label_dk'])




bar_chart = alt.Chart(df).mark_bar(
).transform_filter(
    time_selection
).transform_filter(
    area_selection
).transform_aggregate(
    crime='sum(Anmeldte forbrydelser)',
    groupby=['offence']
).encode(
    x='offence:N',
    y='crime:Q',
    color=alt.condition(
        offence_selection, alt.value('red'), alt.value('lightgray')
    )
).add_selection(offence_selection)



line_chart = alt.Chart(df).mark_line(
).transform_filter(
    offence_selection
).transform_filter(
    area_selection
).transform_aggregate(
    crime='sum(Anmeldte forbrydelser)',
    groupby=['tid']
).encode(
    x='tid:O',
    y='crime:Q'
).add_selection(time_selection)



map_chart = alt.Chart(big_fuck_df).mark_geoshape(
).transform_filter(
    time_selection
).transform_filter(
    offence_selection
).transform_aggregate(
    crime='sum(Anmeldte forbrydelser)',
    groupby=["type","geometry","label_dk"]
).encode(
    color=alt.condition(
        area_selection,
        alt.Color(
            "crime:Q",
            scale=alt.Scale(
                scheme='viridis')
        ),
        alt.value('lightgray'))
).add_selection(area_selection)


chart = bar_chart | line_chart | map_chart
chart.show()

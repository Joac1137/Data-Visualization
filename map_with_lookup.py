import altair as alt
import geopandas as gpd
import pandas as pd
import altair_viewer


alt.data_transformers.enable('data_server')
path = "data/small_few_umbrella_terms_crimes_2021.csv"
df = pd.read_csv(path,encoding="utf_8",index_col='Unnamed: 0')

geometry = gpd.read_file("data_with_geo/geometry.geojson")


map_chart = alt.Chart(df).mark_geoshape(
).transform_aggregate(
    crime='sum(Anmeldte forbrydelser)',
    groupby=["label_dk"]
).transform_lookup(
    lookup='label_dk',
    from_=alt.LookupData(geometry, 'label_dk', ['geometry'])
).encode(
    color=alt.Color(
        "crime:Q",
        scale=alt.Scale(
            scheme='viridis')
    )
)

altair_viewer.show(map_chart)

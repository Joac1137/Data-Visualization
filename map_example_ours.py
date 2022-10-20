import altair as alt
import geopandas as gpd

height = 200
width = 200
spacing = 60


alt.data_transformers.enable('data_server')
file = "small_umbrella_terms_crimes_from_2020"
#file = "small_umbrella_terms_crimes_quarters"

big_fuck_df = gpd.read_file("data_with_geo/" + file +".geojson")


offence_selection = alt.selection_single(init={'offence':'Seksualforbrydelser i alt'})
time_selection = alt.selection_interval(encodings=['x'])
area_selection = alt.selection_single(fields=['label_dk'])



bar_chart = alt.Chart().mark_bar(
).transform_filter(
    time_selection
).transform_filter(
    area_selection
).transform_aggregate(
    crime='sum(Anmeldte forbrydelser)',
    groupby=['offence']
).encode(
    x=alt.X('offence:N', sort='y'),
    y=alt.Y(
        'crime:Q',
        scale=alt.Scale(type="log",domainMin=1)  # Here the scale is applied
    ),
    color=alt.condition(
        offence_selection, alt.value('red'), alt.value('lightgray')
    ),
    tooltip=['offence','crime:Q']
).add_selection(offence_selection).properties(width="container")



line_chart = alt.Chart().mark_line(interpolate='step-after',point=alt.OverlayMarkDef(color="blue")
).transform_filter(
    offence_selection
).transform_filter(
    area_selection
).transform_aggregate(
    crime='sum(Anmeldte forbrydelser)',
    groupby=['tid']
).encode(
    x='tid:O',
    y='crime:Q',
    tooltip=['tid','crime:Q']
).add_selection(time_selection).properties(width="container")



map_chart = alt.Chart().mark_geoshape(
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
        alt.value('lightgray')),
    tooltip=['label_dk','crime:Q']
).add_selection(area_selection).properties(
    height=800,
    width=600
)

column_chart = alt.vconcat(line_chart,bar_chart,spacing=spacing, data=big_fuck_df)

data_chart = alt.hconcat(map_chart,column_chart,data=big_fuck_df, spacing=spacing).resolve_scale(color='independent')


data_chart.show()


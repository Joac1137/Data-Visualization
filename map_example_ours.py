import altair as alt
import pandas as pd
import geopandas as gpd
import altair_viewer

height = 200
width = 200
spacing = 60

alt.data_transformers.enable('data_server')
#file = "umbrella_terms_crimes_quarters"
file = "umbrella_terms_crimes_pop"
#file = "small_umbrella_terms_crimes"
path = "data/" + file +".csv"
df = pd.read_csv(path,encoding="utf_8",index_col='Unnamed: 0')
df['population_scaled'] = df['population'].div(100000)
df['forbrydelser_pr_100k_indbygger'] = df['Anmeldte forbrydelser']/df['population_scaled']
geometry = gpd.read_file("geodata/geometry.geojson")


offence_selection = alt.selection_single(init={'offence':'Seksualforbrydelser i alt'})
time_selection = alt.selection_interval(encodings=['x'])
area_selection = alt.selection_single(fields=['label_dk'])



bars = alt.Chart().mark_bar(
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
    ),
    color=alt.condition(
        offence_selection, alt.value('red'), alt.value('lightgray')
    ),
    tooltip=['offence','crime:Q']
)

text = bars.mark_text(
    align='center',
    baseline='middle',
    dy=-10  # Nudges text to right so it doesn't appear on top of the bar
).encode(
    text='crime:Q'
)
bar_chart = (bars + text).add_selection(offence_selection).properties(width="container")


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
    y=alt.Y('crime:Q',scale=alt.Scale(zero=False)),
    tooltip=['tid','crime:Q'],

).add_selection(time_selection).properties(width=800)



column_select = alt.selection_single(fields=['scale'],
                                     bind=alt.binding_select(options=['crime_pr_100k_inhabitants', 'crime_total'], name='scale'),
                                     init={'scale': 'crime_pr_100k_inhabitants'})


map_chart = alt.Chart().transform_lookup(
    lookup='label_dk',
    from_=alt.LookupData(geometry, 'label_dk',['geometry','type'])
).mark_geoshape(
).transform_filter(
    offence_selection
).transform_filter(
    time_selection
).transform_aggregate(
    crime_total = 'sum(Anmeldte forbrydelser)',
    crime_pr_100k_inhabitants='sum(forbrydelser_pr_100k_indbygger)',
    avg_population = 'mean(population)',
    groupby=["type","geometry","label_dk"]
).transform_fold(
    fold=['crime_pr_100k_inhabitants', 'crime_total'],
    as_=['scale', 'value']
).transform_filter(
    column_select
).encode(
    color=alt.condition(
        area_selection,
        alt.Color(
            "value:Q",
            scale=alt.Scale(
                scheme='viridis')
        ),
        alt.value('lightgray')),
    tooltip=['label_dk','crime_pr_100k_inhabitants:Q','crime_total:Q','avg_population:Q']
).add_selection(area_selection).add_selection(
    column_select
).properties(
    height=800,
    width=600
)

column_chart = alt.vconcat(line_chart,bar_chart,spacing=spacing, data=df)

data_chart = alt.hconcat(map_chart,column_chart,data=df, spacing=spacing).resolve_scale(color='independent')


altair_viewer.show(data_chart)



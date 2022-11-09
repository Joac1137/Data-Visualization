import altair as alt
import pandas as pd
import geopandas as gpd

from IPython.display import display, HTML

display(HTML("""
<style>
form.vega-bindings {
  position: absolute;
  right: 0px;
  top: 0px;
}
</style>
"""))


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
df['tid'] = df['tid'].str.replace('K','-Q')
df['tid'] = pd.to_datetime(df['tid'])
geometry = gpd.read_file("geodata/geometry.geojson")



offence_selection = alt.selection_single(init={'offence':'Seksualforbrydelser i alt'})
time_selection = alt.selection_interval(encodings=['x'])
area_selection = alt.selection_multi(fields=['label_dk'], empty="all")



bars = alt.Chart().mark_bar(
).transform_filter(
    time_selection
).transform_filter(
    area_selection
).transform_aggregate(
    crime='sum(Anmeldte forbrydelser)',
    groupby=['offence']
).encode(
    x=alt.X('offence:N', sort='y',axis=alt.Axis(labelAngle=-20)),
    y=alt.Y(
        'crime:Q',
    ),
    color=alt.condition(
        offence_selection, alt.value('blue'), alt.value('lightgray')
    ),
    tooltip=['offence','crime:Q']
).properties(height=500)

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
    x=alt.X('tid:T',axis=alt.Axis(labelAngle=-30,grid=False)),
    y=alt.Y('crime:Q',scale=alt.Scale(zero=False)),
    #color='label_dk',
    tooltip=['tid','crime:Q'],

).add_selection(time_selection).properties(width=1000, height=200)



column_select = alt.selection_single(fields=['scale'],
                                     bind=alt.binding_select(options=['municipal_crime_pr_100k_inhabitants', 'municipal_crime_total'], name='scale'),
                                     init={'scale': 'municipal_crime_pr_100k_inhabitants'})


map_chart = alt.Chart().transform_lookup(
    lookup='label_dk',
    from_=alt.LookupData(geometry, 'label_dk'),
    as_="geo"
).mark_geoshape(
).transform_filter(
    offence_selection
).transform_filter(
    time_selection
).transform_aggregate(
    municipal_crime_total = 'sum(Anmeldte forbrydelser)',
    municipal_crime_pr_100k_inhabitants='sum(forbrydelser_pr_100k_indbygger)',
    municipal_avg_population = 'mean(population)',
    groupby=["geo","label_dk"]
).transform_fold(
    fold=['municipal_crime_pr_100k_inhabitants', 'municipal_crime_total'],
    as_=['scale', 'value']
).transform_filter(
    column_select
).encode(
    shape="geo:G",
    #strokeWidth=alt.StrokeWidthValue(0, condition=alt.StrokeWidthValue(3, selection=area_selection.name)),
    color= alt.condition(area_selection,alt.Color(
        "value:Q",
        scale=alt.Scale(
            scheme='viridis')
    ),alt.value('lightgray')),
    tooltip=['label_dk','municipal_crime_pr_100k_inhabitants:Q','municipal_crime_total:Q','municipal_avg_population:Q']
).add_selection(area_selection).add_selection(
    column_select
).properties(
    height=500,
    width=500
)




row_chart = alt.hconcat(map_chart,bar_chart, spacing=spacing, data=df).resolve_scale(color='independent')

chart = alt.vconcat(row_chart,line_chart, data=df)

display(chart)


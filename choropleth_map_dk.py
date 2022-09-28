import geopandas as gpd
import altair as alt

# load raw url in geodataframe
url = 'https://raw.githubusercontent.com/magnuslarsen/geoJSON-Danish-municipalities/master/municipalities/municipalities.geojson'
gdf = gpd.read_file(url)

# set projection and reproject
gdf.crs = {'init' :'epsg:27700'}
gdf = gdf.to_crs({'init': 'epsg:4326'})

# define inline geojson data object
data_geojson = alt.InlineData(values=gdf.to_json(), format=alt.DataFormat(property='features',type='json')) 

# chart object
alt.Chart(data_geojson).mark_geoshape(
).encode(
    color=alt.Color(
            "properties.label_dk:N", 
            legend=alt.Legend(
                columns=4),
            scale=alt.Scale(scheme='blues')
            )
    #color=alt.Color("properties.label_en:N", legend=alt.Legend(columns=4))
).show()


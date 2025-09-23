import geopandas as gpd

gdf = gpd.read_file("Korba_Coal_AOI.kml", driver="KML")
gdf.to_file("Korba_Coal_AOI.geojson", driver="GeoJSON")

import geopandas as gpd

gdf = gpd.read_file("/Users/chaitanyakartik/Projects/AgroSpectra/data/GoogleEarth/Korba_Coal_AOI_1.kml", driver="KML")
gdf.to_file("/Users/chaitanyakartik/Projects/AgroSpectra/data/GoogleEarth/Korba_Coal_AOI_1.geojson", driver="GeoJSON")

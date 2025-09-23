import ee
import geopandas as gpd

# --- SETUP: Initialize the Earth Engine API ---
try:
    ee.Initialize(project='agrospectral') 
    print("Google Earth Engine initialized successfully.")
except ee.EEException:
    print("Authentication failed. Please run 'earthengine authenticate' in your terminal.")
    exit()

# --- STEP 1: Load your local Area of Interest (AOI) ---
# Use the path to your KML or GeoJSON file.
# Make sure this file is in the same directory or provide the full path.
aoi_file_path = '/Users/chaitanyakartik/Projects/AgroSpectra/data/GoogleEarth/Korba_Coal_AOI_1.kml' # Or your .geojson file
gdf = gpd.read_file(aoi_file_path, driver='KML')

# Convert the GeoPandas geometry to an Earth Engine Geometry object
# We'll just use the first polygon found in the file
aoi_geom = gdf.geometry.iloc[0]
min_lon, min_lat, max_lon, max_lat = aoi_geom.bounds
ee_aoi = ee.Geometry.Rectangle([min_lon, min_lat, max_lon, max_lat])

print(f"Successfully loaded AOI from: {aoi_file_path}")


# --- STEP 2: Search, Filter, and Select an Image ---
# All of this happens on Google's servers.
image_collection = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') # Sentinel-2 L2A data
                    .filterBounds(ee_aoi) # Find images covering our AOI
                    .filterDate('2025-01-01', '2025-04-30') # Filter by date
                    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10)) # Filter by cloud cover
                    .sort('CLOUDY_PIXEL_PERCENTAGE')) # Sort to get the clearest image

# Check if any images were found
if image_collection.size().getInfo() == 0:
    print("No images found for the specified criteria. Try a different date range.")
    exit()

# Select the very best image (the one with the least clouds)
best_image = ee.Image(image_collection.first())
print(f"Found best image: {best_image.id().getInfo()}")


# --- STEP 3: Process the Image in the Cloud ---
# Select only the bands you need and clip it to your exact AOI
bands_to_select = ['B4', 'B8', 'B11'] # Red, NIR, SWIR
clipped_image = best_image.select(bands_to_select).clip(ee_aoi)

print("Image processing (band selection and clipping) complete on GEE servers.")


# --- STEP 4: Get a Download Link for Your Small, Processed Image ---
# This generates a URL to download a GeoTIFF file.
# The 'scale' parameter sets the resolution in meters (10 is highest for these bands).
download_url = clipped_image.getDownloadURL({
    'scale': 10,
    'crs': 'EPSG:4326',
    'region': ee_aoi.toGeoJSONString(),
    'fileFormat': 'GeoTIFF'
})

print("\n--- DOWNLOAD ---")
print("Copy and paste this URL into your browser to download your processed image:")
print(download_url)
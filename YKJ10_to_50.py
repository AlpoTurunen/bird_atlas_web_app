import geopandas as gpd
import numpy as np

# Load the 10 km grid shapefile
grid_10km = gpd.read_file("data/YKJ10000_polygons.shp")

# Ensure CRS is correct (YKJ grid should be EPSG:2393)
if grid_10km.crs is None:
    grid_10km.set_crs(epsg=2393, inplace=True)  # YKJ Grid CRS

# Function to generate 50 km grid ID based on 10 km grid coordinates
def generate_50km_grid_id(x, y):
    return f"{(x // 50000) * 50000}_{(y // 50000) * 50000}"

# Extract centroid coordinates for aggregation
grid_10km["centroid"] = grid_10km.geometry.centroid
grid_10km["grid_x"] = grid_10km["centroid"].x
grid_10km["grid_y"] = grid_10km["centroid"].y

# Create new 50 km grid ID
grid_10km["grid_50km_id"] = grid_10km.apply(lambda row: generate_50km_grid_id(row["grid_x"], row["grid_y"]), axis=1)

# Dissolve (merge) smaller grids into 50 km x 50 km blocks
grid_50km = grid_10km.dissolve(by="grid_50km_id")

grid_50km = grid_50km.drop(columns=["centroid", "grid_x", "grid_y"])

# Save as new shapefile
grid_50km.to_file("ykj_50km_grid.gpkg", driver="GPKG", geometry="geometry")

print("50 km grid saved as 'ykj_50km_grid.gpkg'")

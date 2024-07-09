import os
import geopandas as gpd

# This script downloads the US County Data needed in the dataprep.py script
# NB: you'll need to be on a VPN to the US in order to pass the geo restrictions of census.gov
print('Downloading US county data from census.gov')

# Create the directory if it doesn't exist
output_dir = 'data/us_geo'
os.makedirs(output_dir, exist_ok=True)

# Define the URL for the US counties shapefile
url_counties = 'https://www2.census.gov/geo/tiger/GENZ2020/shp/cb_2020_us_county_20m.zip'

# Download and save the shapefile
gdf_counties = gpd.read_file(url_counties)

# Save to the specified directory
output_file = os.path.join(output_dir, 'us_counties.shp')
gdf_counties.to_file(output_file)

# Save as CSV
output_csv = os.path.join(output_dir, 'us_counties.csv')
gdf_counties.drop(columns='geometry').to_csv(output_csv, index=False)

# Read the shapefile from the saved location
counties = gpd.read_file(output_file)

# Display the first few rows of the counties GeoDataFrame
print('Sample rows of output')
print(counties.head())

print('Finished downloading data')
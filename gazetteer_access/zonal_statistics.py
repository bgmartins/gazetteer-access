import sqlite3
import urllib
import gzip
import bz2
import rasterio
import rasterstats
import pkg_resources
from .geocode import geocode_placename

def zonal_statistics( name , raster, stats=['min', 'max', 'mean', 'median', 'majority', 'minority', 'unique', 'count', 'sum', 'std']):
    raster_data = rasterio.open(raster)
    polygon = geocode_placename(name)
    polygon = polygon.to_crs(crs=dem.crs.data)
    array = raster_data.read(1)
    affine = raster_data.affine
    stats = rasterstats.zonal_stats(polygon, array, affine=affine, stats=stats, geojson_out=True)
    return stats

if __name__ == "__main__":
    aux = geocode_placename("Lisbon", "gpw_v4_population_count_rev11_2020_30_sec.tif")
    GeoJSONFeatureCollectionAsString = geojson.dumps(aux)
    print(GeoJSONFeatureCollectionAsString)



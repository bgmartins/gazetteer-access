import spatialite
import urllib
import gzip
import bz2
import rasterio
import rasterstats

dem = rasterio.open(dem_fp)
polygon = kallio.to_crs(crs=dem.crs.data)

array = dem.read(1)
affine = dem.affine
kallio = rasterstats.zonal_stats(polygon, array, affine=affine, stats=['min', 'max', 'mean', 'median', 'majority', 'minority', 'unique', 'count', 'sum', 'std'], geojson_out=True)



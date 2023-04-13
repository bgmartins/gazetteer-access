import spatialite
import urllib
import gzip
import bz2

def reverse_geocode( lat, lon, EPSG=32632, onlyFirst = True ):
    connection = spatialite.connect("gazetteer.db")
    cursor = connection.execute("select name, geonamesID, AsGeoJSON(geometry) from gazetteer where ST_Intersects(geometry, ST_GeomFromText('POINT (?)',32632))", (lat, lon))
    featureCollection = list()
    for row in cursor:
        geom = geojson.loads(row['AsGeoJSON(geometry)'])
        row.pop('AsGeoJSON(geometry)')
        feature = geojson.Feature(geometry=geom, properties=row)
        featureCollection.append(feature)
        if onlyFirst: break
    connection.close()
    return featureCollection



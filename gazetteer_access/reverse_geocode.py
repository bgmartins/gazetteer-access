import sqlite3
import geojson
import pkg_resources

def reverse_geocode_point( lat, lon, EPSG=32632, onlyFirst = True ):
    db = pkg_resources.resource_filename(__name__, 'gazetteer.db')
    connection = sqlite3.connect(db)
    cursor = connection.execute("SELECT DISTINCT AsGeoJSON(geometry.geom), place.id, place.type FROM place, search, geometry WHERE place.id=search.id AND place.source=search.source AND place.id=geometry.id AND place.source=geometry.source AND ST_Intersects(geometry.geom, ST_GeomFromText('POINT (?)',32632)) AND geometry.role='boundary' ORDER BY Area(geometry.geom) ASC;", (lat, lon) )
    featureCollection = list()
    for row in cursor:
        row = row.dict()
        geom = geojson.loads(row['AsGeoJSON(geometry.geom)'])
        row.pop('AsGeoJSON(geometry.geom)')
        feature = geojson.Feature(geometry=geom, properties=row)
        featureCollection.append(feature)
        if onlyFirst: break
    connection.close()
    return featureCollection

if __name__ == "__main__":
    aux = reverse_geocode_point(38.7223, -9.1393)
    GeoJSONFeatureCollectionAsString = geojson.dumps(aux)
    print(GeoJSONFeatureCollectionAsString)
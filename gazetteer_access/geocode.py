import sqlite3
import geojson
import pkg_resources

def geocode_placename(name , type=None, onlyFirst=True, centroid=False):
    db = pkg_resources.resource_filename(__name__, 'gazetteer.db')
    connection = spatialite.connect(db)
    if centroid:
        cursor = connection.execute("SELECT DISTINCT AsGeoJSON(geometry.geom), place.id, place.type FROM place, search, geometry WHERE place.id=search.id AND place.source=search.source AND place.id=geometry.id AND place.source=geometry.source AND name=? AND geometry.role='centroid';", (name,) )
    else:
        cursor = connection.execute("SELECT DISTINCT AsGeoJSON(geometry.geom), place.id, place.type FROM place, search, geometry WHERE place.id=search.id AND place.source=search.source AND place.id=geometry.id AND place.source=geometry.source AND name=? AND geometry.role='boundary' ORDER BY Area(geometry.geom) DESC;", (name,) )
    featureCollection = list()
    for row in cursor:
        row = row.dict()
        geom = geojson.loads(row['AsGeoJSON(geometry.geom)'])
        row.pop('AsGeoJSON(geometry.geom)')
        feature = geojson.Feature(geometry=geom, properties=row)
        featureCollection.append(feature)
        if onlyFirst: break
    connection.close()
    if len(featureCollection) == 0 and not(centroid): return geocode_placename(name , type, onlyFirst, centroid=True)
    return featureCollection

if __name__ == "__main__":
    aux = geocode_placename("Lisbon")
    GeoJSONFeatureCollectionAsString = geojson.dumps(aux)
    print(GeoJSONFeatureCollectionAsString)


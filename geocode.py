import spatialite
import geojson
import urllib
import gzip
import bz2

def geocode_placename( name , onlyFirst = True ):
    connection = spatialite.connect('gazetteer.db')
    cursor = connection.execute('SELECT AsGeoJSON(geometry), geonamesID FROM gazetteer WHERE name = ? ORDER BY Area(geometry)', (name,))
    featureCollection = list()
    for row in cursor:
        geom = geojson.loads(row['AsGeoJSON(geometry)'])
        row.pop('AsGeoJSON(geometry)')
        feature = geojson.Feature(geometry=geom, properties=row)
        featureCollection.append(feature)
        if onlyFirst: break
    connection.close()
    return featureCollection

def geocode_placename( name , type , onlyFirst = True ):
    return geocode(name)

if __name__ == "__main__":
    aux = geocode("Kallio")
    GeoJSONFeatureCollectionAsString = geojson.dumps(aux)
    print(GeoJSONFeatureCollectionAsString)


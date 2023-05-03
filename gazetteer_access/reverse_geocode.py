import sqlite3
import geojson
import pkg_resources
import fiona
import pyproj
from shapely import geometry

def reverse_geocode_point( lat, lon, EPSG=32632, onlyFirst = True, vectorNet = True, geoJSON = True ):
    if vectorNet:
        shapefile = pkg_resources.resource_filename(__name__, 'vectornet_polygons/VectornetDATAforMOOD.shp')
        shapes = fiona.open(shapefile)
        featureCollection = list()
        p = geometry.Point(lon, lat)
        for region in shapes:
            s = geometry.shape(region["geometry"])
            if s.contains(p): 
                featureCollection.append(region)
                break
    else:
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
    if geoJSON: featureCollection = geojson.dumps(featureCollection)
    return featureCollection

def reverse_geocode_geometry( polygonal_region , EPSG=32632, onlyFirst = True, vectorNet = True, geoJSON = True ):
    if vectorNet:
        shapefile = pkg_resources.resource_filename(__name__, 'vectornet_polygons/VectornetDATAforMOOD.shp')
        shapes = fiona.open(shapefile)
        featureCollection = list()
        p = geometry.shape(polygonal_region)
        max_area = 0
        for region in shapes:
            s = geometry.shape(region["geometry"])
            area = s.intersection(p).area / p.area
            if area > max_area: 
                featureCollection.pop()
                featureCollection.append(region)
    else:
        db = pkg_resources.resource_filename(__name__, 'gazetteer.db')
        connection = sqlite3.connect(db)
        cursor = connection.execute("SELECT DISTINCT AsGeoJSON(geometry.geom), place.id, place.type FROM place, search, geometry WHERE place.id=search.id AND place.source=search.source AND place.id=geometry.id AND place.source=geometry.source AND ST_Intersects(geometry.geom, ST_GeomFromText('?',32632)) AND geometry.role='boundary' ORDER BY Area(geometry.geom) ASC;", (geometry) )
        featureCollection = list()
        for row in cursor:
            row = row.dict()
            geom = geojson.loads(row['AsGeoJSON(geometry.geom)'])
            row.pop('AsGeoJSON(geometry.geom)')
            feature = geojson.Feature(geometry=geom, properties=row)
            featureCollection.append(feature)
            if onlyFirst: break
        connection.close()
    if geoJSON: featureCollection = geojson.dumps(featureCollection)
    return featureCollection

if __name__ == "__main__":
    aux = reverse_geocode_point(38.7223, -9.1393)    
    print(aux)
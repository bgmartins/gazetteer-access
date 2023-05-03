import sqlite3
import geojson
import pkg_resources
import fiona
import pyproj
from shapely import geometry

_vectornet_shapefile = pkg_resources.resource_filename(__name__, 'vectornet_polygons/VectornetDATAforMOOD.shp')
_vectornet_shapes = fiona.open(_vectornet_shapefile)

def reverse_geocode_point( lat, lon, EPSG=32632, onlyFirst = True, vectornet = True, geoJSONString = True ):
    if vectornet:
        featureCollection = list()
        p = geometry.Point(lon, lat)
        for region in _vectornet_shapes:
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
    if geoJSONString: featureCollection = geojson.dumps(featureCollection, indent=1)
    return featureCollection

def reverse_geocode_geometry( polygonal_region , EPSG=32632, onlyFirst = True, vectornet = True, geoJSONString = True ):
    if vectornet:
        featureCollection = list()
        if isinstance(polygonal_region, str):
            try: 
                p = shapely.wkt.loads(polygonal_region)
            except: 
                p = geometry.shape(geojson.loads(polygonal_region))
        else: p = geometry.shape(polygonal_region)
        max_area = 0
        for region in _vectornet_shapes:
            s = geometry.shape(region["geometry"])
            area = s.intersection(p).area / p.area
            if area > max_area: 
                if featureCollection: featureCollection.pop()
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
    if geoJSONString: featureCollection = geojson.dumps(featureCollection, indent=1)
    return featureCollection

if __name__ == "__main__":
    print("Test the reverse geocoding of a point corresponding to Lisbon, Portugal...")
    result = reverse_geocode_point(38.7223, -9.1393)
    print(result)
    print()

    print("Test the reverse geocoding of a geometry that approximates the boundary of Lisbon, Portugal...")
    geom = {
        "type": "Polygon",
        "coordinates": [ [ [-9.2242, 38.6916], [-9.2394, 38.7267], [-9.1683, 38.7397], [-9.1355, 38.7209], [-9.1417, 38.6974], [-9.2242, 38.6916] ] ]
    }
    result = reverse_geocode_geometry(geom)
    print(result)
    print()
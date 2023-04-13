
import sqlite3
import requests

wof_data = "https://data.geocode.earth/wof/dist/spatial/whosonfirst-data-admin-latest.spatial.db.bz2"

def read_file_from_uri(uri):
    if uri.startswith('http'):
        file = urllib.request.urlopen(uri)
    else:
        file = open(uri, 'r')
    if uri.endswith('.gz'):
        file = gzip.open(file, 'rt')
    return file

def download_file(url, filename):
    with open(filename, 'wb') as f:
        f.write(requests.get(url).content)

def create_database(filename):
    download_file(wof_data, filename )
    conn = sqlite3.connect(filename)
    # Lead the spatialite extension:
    conn.enable_load_extension(True)
    conn.load_extension("/usr/local/lib/mod_spatialite.dylib")
    conn.execute("select InitSpatialMetadata(1)")
    conn.executescript("create table gazetteer (id integer primary key, name text, population integer, type text)")
    conn.execute("SELECT AddGeometryColumn('gazetteer', 'point_geometry', 4326, 'POINT', 2);")
    conn.execute("SELECT AddGeometryColumn('gazetteer', 'geometry', 4326, 'POINT', 2);")
    conn.execute("SELECT CreateSpatialIndex('gazetteer', 'point_geometry');")    
    conn.execute("SELECT CreateSpatialIndex('gazetteer', 'geometry');")
    conn.commit()
    conn.execute("vacuum")
    conn.close()

if __name__ == "__main__":
    create_database("gazetteer.db")
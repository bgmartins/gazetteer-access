import spatialite
import urllib
import gzip
import bz2

#
# Gazetteer data from https://geocode.earth/data/whosonfirst/combined/
#
wof_data = "https://data.geocode.earth/wof/dist/spatial/whosonfirst-data-admin-latest.spatial.db.bz2"
pop_data = "https://sedac.ciesin.columbia.edu/downloads/data/gpw-v4/gpw-v4-population-count-rev11/gpw-v4-population-count-rev11_2020_30_sec_tif.zip"

def read_file_from_uri(uri):
    if uri.startswith('http'):
        file = urllib.request.urlopen(uri)
    else:
        file = open(uri, 'r')
    if uri.endswith('.gz'):
        file = gzip.open(file, 'rt')
    if uri.endswith('.bz2'):
        file = bz2.open(file, 'rt')        
    return file

def download_file(url, filename):
    with open(filename, 'wb') as f:
        f.write(read_file_from_uri(url).read())

def create_database(filename):
    download_file(wof_data, filename)
    conn = spatialite.connect(filename)
    # Lead the spatialite extension:
    #conn.enable_load_extension(True)
    #conn.load_extension("/usr/local/lib/mod_spatialite.dylib")
    #conn.execute("select InitSpatialMetadata(1)")
    #conn.executescript("create table my_gazetteer (id integer primary key, name text, population integer, type text)")
    #conn.execute("SELECT AddGeometryColumn('gazetteer', 'point_geometry', 4326, 'POINT', 2);")
    #conn.execute("SELECT AddGeometryColumn('gazetteer', 'geometry', 4326, 'MULTIPOLYGON', 2);")
    #conn.execute("SELECT CreateSpatialIndex('gazetteer', 'point_geometry');")    
    #conn.execute("SELECT CreateSpatialIndex('gazetteer', 'geometry');")
    #conn.commit()
    #conn.execute("vacuum")
    #conn.close()

def check_database(filename):
    sqliteConnection = spatialite.connect(filename)
    print("Connected to SQLite")
    sql_query = """SELECT name FROM sqlite_master WHERE type='table';"""
    cursor = sqliteConnection.cursor()
    cursor.execute(sql_query)
    print("List of tables\n")
    print(cursor.fetchall())
    cursor = sqliteConnection.execute('select * from Student;')
    names = list(map(lambda x: x[0], cursor.description))
    sqliteConnection.close()
    print(names)    

if __name__ == "__main__":
    # create_database("gazetteer.db")
    check_database("gazetteer.db")









import spatialite
import urllib
import gzip
import bz2

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
    print("Doenloading data from https://geocode.earth/data/whosonfirst/combined/")
    download_file(wof_data, filename)
    conn = spatialite.connect(filename)
    conn.commit()
    conn.execute("vacuum")
    conn.close()

if __name__ == "__main__":
    create_database("gazetteer.db")
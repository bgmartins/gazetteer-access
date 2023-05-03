import pkg_resources
import sqlite3
import urllib
import gzip
import bz2
import logging
import sys
import os
import tempfile
from zipfile import ZipFile
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install

wof_data = "https://data.geocode.earth/wof/dist/spatial/whosonfirst-data-admin-latest.spatial.db.bz2"
pop_data = "https://sedac.ciesin.columbia.edu/downloads/data/gpw-v4/gpw-v4-population-count-rev11/gpw-v4-population-count-rev11_2020_30_sec_tif.zip"

logging.basicConfig(stream=sys.stderr, level=logging.INFO)
log = logging.getLogger()

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

def create_population(filename):
    log.info("Downloading data from https://sedac.ciesin.columbia.edu")
    aux = urllib.parse.urlparse(pop_data)
    file = urllib.request.urlopen(pop_data)
    temp = tempfile.NamedTemporaryFile()
    temp.write(file.read())
    temp.close()
    with ZipFile(temp.name, 'r') as zipObj:
        aux = urllib.parse.urlparse(pop_data)
        extract_file = os.path.basename(aux.path).replace(".zip","")
        zipObj.extract(extract_file, path=filename, pwd=None)

def create_database(filename):
    log.info("Downloading data from https://geocode.earth/data/whosonfirst/combined/")
    download_file(wof_data, filename)
    conn = sqlite3.connect(filename)
    conn.commit()
    conn.execute("vacuum")
    conn.close()

class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        develop.run(self)
        #po = pkg_resources.resource_filename(__name__, 'population.tif')
        #create_population(po)
        #db = pkg_resources.resource_filename(__name__, 'gazetteer.db')
        #create_database(db)

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        #po = pkg_resources.resource_filename(__name__, 'population.tif')
        #create_population(po)
        #db = pkg_resources.resource_filename(__name__, 'gazetteer.db')
        #create_database(db)        

setup(
    name='gazetteer_access',
    version='0.1.0',    
    description="Simple Python library supporting the access to the who's on first gazetteer data.",
    url='https://github.com/bgmartins/gazetteer-access',
    author='Bruno Martins',
    author_email='bgmartins@gmail.com',
    license='BSD 2-clause',
    packages=['gazetteer_access'],
    install_requires=['rasterio', 'rasterstats', 'spatialite', 'geojson', 'parsedatetime', 'nuts-finder', 'shapely', 'fiona', 'pyproj' ],
    include_package_data=True,
    package_data={'': ['vectornet_polygons/*']},
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
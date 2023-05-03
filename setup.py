import pkg_resources
import sqlite3
import urllib
import gzip
import bz2
from zipfile import ZipFile
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install

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

#def create_population(username, password, filename):
#    filename = os.path.basename(urlparse(pop_data).path)
#    r = requests.get(url, auth=(username,password))
#    with ZipFile(r, 'r') as zipObj:
#        zipObj.extract("", path=filename, pwd=None)

def create_database(filename):
    print("Downloading data from https://geocode.earth/data/whosonfirst/combined/", file=sys.stderr)
    #download_file(wof_data, filename)
    conn = sqlite3.connect(filename)
    conn.commit()
    conn.execute("vacuum")
    conn.close()

class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        develop.run(self)
        db = pkg_resources.resource_filename(__name__, 'gazetteer.db')
        create_database(db)

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        db = pkg_resources.resource_filename(__name__, 'gazetteer.db')
        create_database(db)        

setup(
    name='gazetteer_access',
    version='0.1.0',    
    description="Simple Python library supporting the access to the who's on first gazetteer data.",
    url='https://github.com/bgmartins/gazetteer-access',
    author='Bruno Martins',
    author_email='bgmartins@gmail.com',
    license='BSD 2-clause',
    packages=['gazetteer_access'],
    install_requires=['rasterio', 'rasterstats', 'spatialite', 'geojson', 'requests' ],
    include_package_data=True,
    package_data={'': ['*.db']},
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
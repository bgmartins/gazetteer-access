# gazetteer_access

Simple Python library supporting the access to the [who's on first gazetteer data](https://geocode.earth/data/whosonfirst/combined/). 

* Convert placenames into structured geographic information (i.e., geocode place names into GeoJSON geometries).
* Convert point locations of GeoJSON geometries into placenames (i.e., reverse geocoding).
* Compute zonal statistics from placenames and raster data.

**Currently under development!** 

Installation
-------------

```
pip install git+https://github.com/bgmartins/gazetteer-access
```

Example usage
-------------

```
>>> import gazetteer_access as ga
>>> ga.reverse_geocode_point(38.7223, -9.1393)
>>> ga.geocode_placename("Lisbon")
```

**Note**: It's *strongly* recommended that you run this library in a virtual environment. The libraries that gazetteer-access depends on are not always the most recent versions and using a virtual environment prevents libraries from being downgraded or running into other issues.

How does it work?
-----------------

gazetteer_access uses a [sqlite](https://sqlite.org/index.html) database with the data from the [who's on first gazetteer data](https://geocode.earth/data/whosonfirst/combined/). 
The gazetter entries are complemented with population statistics derived from the [Gridded Population of the World](https://sedac.ciesin.columbia.edu/data/collection/gpw-v4) dataset. 

- Geocoding takes placenames as input and returns poligonal boundaries from the matching gazetteer entries, giving preference to highly populated places.

- Reverse geocoding uses point-in-polygon or polygon intersection queries over the gazetteer entries.

- Zonal statistics (e.g., averages or sums over poligonal boundaries) can be computed from raster data with basis on place names. Geocoding is used to transform the placenames into poligonal boundaries, and the [rasterstats](https://pythonhosted.org/rasterstats/) Python package is then used to compute the aggregate statistics.

# gazetteer-access

Simple Python library supporting the access to the [who's on first gazetteer data](https://geocode.earth/data/whosonfirst/combined/). 

* Convert placenames into structured geographic information (i.e., geocode place names into GeoJSON geometries).
* Convert point locations of GeoJSON geometries into placenames (i.e., reverse geocoding).
* Compute zonal statistics from placenames and raster data.

**Currently under development!** 

Example usage
-------------

```
>>> from mordecai import Geoparser
>>> geo = Geoparser()
>>> geo.geoparse("I traveled from Oxford to Ottawa.")

[{'country_conf': 0.96474487,
  'country_predicted': 'GBR',
  'geo': {'admin1': 'England',
   'country_code3': 'GBR',
   'feature_class': 'P',
   'feature_code': 'PPLA2',
   'geonameid': '2640729',
   'lat': '51.75222',
   'lon': '-1.25596',
   'place_name': 'Oxford'},
  'spans': [{'end': 22, 'start': 16}],
  'word': 'Oxford'},
 {'country_conf': 0.83302397,
  'country_predicted': 'CAN',
  'geo': {'admin1': 'Ontario',
   'country_code3': 'CAN',
   'feature_class': 'P',
   'feature_code': 'PPLC',
   'geonameid': '6094817',
   'lat': '45.41117',
   'lon': '-75.69812',
   'place_name': 'Ottawa'},
  'spans': [{'end': 32, 'start': 26}],
  'word': 'Ottawa'}]
```

**Note**: It's *strongly* recommended that you run this library in a virtual environment. The libraries that gazetteer-access depends on are not always the most recent versions and using a virtual environment prevents libraries from being downgraded or running into other issues.

How does it work?
-----------------

gazetteer-access uses a [sqlite](https://sqlite.org/index.html) database with the data from the [who's on first gazetteer data](https://geocode.earth/data/whosonfirst/combined/). 
The gazetter entries are complemented with population statistics derived from the [Gridded Population of the World](https://sedac.ciesin.columbia.edu/data/collection/gpw-v4) dataset. 

- Geocoding takes placenames as input and returns poligonal boundaries from the matching gazetteer entries, giving preference to highly populated places.

- Reverse geocoding uses point-in-polygon or polygon intersection queries over the gazetteer entries.

- Zonal statistics (e.g., averages or sums over poligonal boundaries) can be computed from raster data with basis on place names. Geocoding is used to transform the placenames into poligonal boundaries, and the [rasterstats](https://pythonhosted.org/rasterstats/) Python package is then used to compute the aggregate statistics.

# gazetteer-access

Simple Python library supporting the access to the [who's on first gazetteer data|https://geocode.earth/data/whosonfirst/combined/]. 

* Convert place names into structured geographic information (i.e., geocode place names into GeoJSON geometries).
* Convert point locations of GeoJSON geometries into place names (i.e., reverse geocoding).
* Compute zonal statistics from place names and raster data.

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

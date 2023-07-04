#!/usr/bin/env python
import json
import logging

import geopy.distance
import pyproj
import requests

logger = logging.getLogger(__name__)


def coord_distance(coords_1, coords_2):
	"""Calculate geodesic distance between 2 GPS points.
	"""
	return geopy.distance.geodesic(coords_1, coords_2).km


def get_coordinates(municipality):
	"""Given a municipality, get its GPS coordinates.

	:param		municipality:		Municipality
	:type		municipality:		str
	:return		(long, lat):		GPS longitude, GPS latitude
	:rtype		(long, lat):		(float, float)
	"""

	url = f'https://api-adresse.data.gouv.fr/search/?q={municipality}&type=municipality'
	try:
		response = requests.get(url)
	except requests.exceptions.RequestException as err:
		logger.error(f"Could not retrieve data from url '{url}'. Cause: {err}")	
		raise Exception("Could not retrieve data")

	try:
		data = json.loads(response.text) 
	except json.JSONDecodeError:
		logger.error(f"API data is not a valid JSON document. Data: {response.text}. Cause: '{err}'")
		raise Exception("API data is not a valid JSON document")

	try:
		coords = data['features'][0]['geometry']['coordinates']
	except Exception as err:
		logger.error(f"Wrongly formatted API data. Data: {data}. Cause: '{err}'")
		raise Exception("Wrongly formatted API data")

	return coords


def lamber93_to_gps(x, y):
	lambert = pyproj.Proj('+proj=lcc +lat_1=49 +lat_2=44 +lat_0=46.5 +lon_0=3 +x_0=700000 +y_0=6600000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs')
	wgs84 = pyproj.Proj('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')
	#x = 102980
	#y = 6847973
	long, lat = pyproj.transform(lambert, wgs84, x, y)
	return long, lat

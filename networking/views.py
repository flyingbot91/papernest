#!/usr/bin/env python
import logging

from django.http import JsonResponse

from networking.models import Operator, Site
from networking.utils import coord_distance, get_coordinates

logger = logging.getLogger(__name__)


def coverage(request, q):
	# Basic response data
	rdata = {
		"operators": {},
		"error": None
	}

	try:
		coords = get_coordinates(q)
	except Exception as err:
		rdata["error"] = f"{err}" 
		return JsonResponse(rdata)
	
	logger.info(f"Coords for {q}: {coords}")

	for operator in Operator.objects.all():
		sites = Site.objects.filter(operator=operator)
		if not sites.exists():
			continue

		closest = sites.first()
		aux = 999999999
		for site in sites:
			dist = coord_distance(coords, (site.coord_x, site.coord_y))
			if dist < aux:
				closest = site
				aux = dist

		logger.info(closest.operator.name, closest.coord_x, closest.coord_y, aux)
		rdata["operators"][closest.operator.name] = {
			"2G": closest.mt_2g,
			"3G": closest.mt_3g,
			"4G": closest.mt_4g
		}
	
	return JsonResponse(rdata)

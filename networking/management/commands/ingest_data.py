import os

import requests
from bs4 import BeautifulSoup

from django.core.management.base import BaseCommand, CommandError

from networking.models import Operator, Site
from networking.utils import lamber93_to_gps


class Command(BaseCommand):
	help = "Ingest site dat from CSV file"

	def add_arguments(self, parser):
		parser.add_argument(
			"csv_file", 
			type=str,
			help="CSV file with site data to be ingested"
		)

	def handle(self, *args, **options):
		csv_file = options.get('csv_file')

		if not os.path.exists(csv_file):
			raise CommandError(f"File {csv_file} does not exist")

		self.ingest_operators()
		self.ingest_csv(csv_file)

	def ingest_operators(self):
		url = 'https://fr.wikipedia.org/wiki/Mobile_Network_Code'
		data = requests.get(url)
		soup = BeautifulSoup(data.text, 'html.parser')
		table = soup.find('table', attrs={'class': 'wikitable'})
		rows = table.findAll('tr')
		operators = []
		# Ignore the header line
		for row in rows[1:]:
			cells = row.findAll('td')
			code = f"{cells[0].text.strip()}{cells[1].text.strip()}"
			name = f"{cells[3].text.strip()}"
			operators.append(
				Operator(
					code=code,
					name=name
				)
			)

		# Persist data
		objs = Operator.objects.bulk_create(operators)

	def ingest_csv(self, csv_file):
		operators = {item[0]: item[1] for item in Operator.objects.values_list('code', 'pk')}
		print(operators)
		with open(csv_file) as f:
			# Ignore the header line
			lines = f.readlines()[1:]
			num_lines = len(lines) 
			for idx, line in enumerate(lines):
				data = line.strip().split(';')
				try:
					gps_x, gps_y = lamber93_to_gps(data[1], data[2])
					print(data[1], data[2])
					print(gps_x, gps_y)
				except TypeError as err:
					print(idx, data)
					continue
		
				try:
					obj = Site.objects.create(
						operator_id=operators[data[0]],
						coord_x=gps_x,
						coord_y=gps_y,
						mt_2g=data[3],
						mt_3g=data[4],
						mt_4g=data[5],
					)
				except Exception as err:
					print(idx, data)
					continue

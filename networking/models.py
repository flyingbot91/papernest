from django.db import models


class Operator(models.Model):
	name = models.CharField(max_length=40)
	code = models.CharField(max_length=5)

	def __str__(self):
		return f"{self.name} - {self.code}"


class Site(models.Model):
	operator = models.ForeignKey("Operator", on_delete=models.CASCADE)
	coord_x = models.FloatField()
	coord_y = models.FloatField()
	mt_2g = models.BooleanField()
	mt_3g = models.BooleanField()
	mt_4g = models.BooleanField()

	def __str__(self):
		return f"{self.operator} ({self.coord_x}, {self.coord_y}) " \
			f"{int(self.mt_2g)}{int(self.mt_3g)}{int(self.mt_4g)}"

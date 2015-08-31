from django.db import models

class SalesforceDomainEntry(models.Model):
	category = models.CharField(max_length=255, default='')
	domain = models.CharField(max_length=255, default='', unique=True)

	def __str__(self):
		return "<%s: %s>"%(self.category, self.domain)

from django.db import models

# Create your models here.
class dbFile(models.Model):
	file = models.FileField(blank=False, null=False)
	timestamp = models.DateTimeField(auto_now_add=True)

# importing models from Django
from django.db import models

# defining our class for Animal- our Animal Sounds plugin
class Animal(models.Model):
	# specifying attributes that will have columns in our new table
	name = models.CharField(max_length=50)
	sound = models.CharField(max_length=50)

	''' we learned about this in Learn Python: Classes.
	This class will give us detailed return string, in this case,
	just the instance name, if we directly print or output the instance.'''
	def __str__(self):
		return self.name
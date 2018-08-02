from django.db import models



class Category(models.Model):
	name = models.CharField(max_length=100, unique=True)



class Product(models.Model):
	name = models.CharField(max_length=100, unique=True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	description = models.CharField(max_length=1000)
	nutriscore = models.IntegerField(null=False)
	picture = models.URLField()

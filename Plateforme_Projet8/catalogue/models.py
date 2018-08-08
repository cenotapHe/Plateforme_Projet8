from django.db import models

from django.contrib.auth.models import User


class Category(models.Model):
	name = models.CharField(max_length=100, unique=True)



class Product(models.Model):
	name = models.CharField(max_length=100, unique=True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	description = models.CharField(max_length=1000)
	nutriscore = models.IntegerField(null=False)
	picture = models.URLField(null=False)
	nutrition = models.URLField(null=False)
	url_off = models.URLField(null=False)



class Association(models.Model):
	asso_user = models.IntegerField(null=False)
	asso_product = models.IntegerField(null=False)
	asso_product_sub = models.IntegerField(null=False)
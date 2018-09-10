from django.db import models

# import the class User
# Django manage the user
from django.contrib.auth.models import User


# Category regroup many product for comparaison
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

# Product represent each product in the database


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)
    nutriscore = models.IntegerField(null=False)
    picture = models.URLField(null=False)
    nutrition = models.URLField(null=False)
    url_off = models.URLField(null=False)


# Association permite subsitute for a product by each user for a new product
class Association(models.Model):
    asso_user = models.ForeignKey(User, on_delete=models.CASCADE)
    asso_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    asso_product_sub = models.IntegerField(null=False)

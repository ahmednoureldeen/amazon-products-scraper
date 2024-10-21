from django.db import models

# Create your models here.

class Brand(models.Model):
  name = models.CharField(unique=True, max_length=255)
    
  def __str__(self):
    return self.name  

class Product(models.Model):
  brand = models.ForeignKey(to=Brand, on_delete=models.PROTECT)
  name = models.CharField(max_length=255, unique=True)
  asin = models.CharField(max_length=255)
  sku = models.CharField(max_length=255, null=True)
  image_url = models.CharField(max_length=1024)

  def __str__(self):
    return self.name

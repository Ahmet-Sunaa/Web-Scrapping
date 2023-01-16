from django.db import models

class Products(models.Model):
    title=models.CharField(max_length=200,blank=True)
    brand=models.CharField(max_length=20,blank=True)
    model=models.CharField(max_length=50,blank=True)
    operating_system=models.CharField(max_length=10,blank=True)
    processor_model=models.CharField(max_length=10,blank=True)
    processor_generation=models.CharField(max_length=5,blank=True)
    ram=models.CharField(max_length=10,blank=True)
    disk_size=models.CharField(max_length=10,blank=True)
    disk_type=models.CharField(max_length=10,blank=True)
    screen_size=models.CharField(max_length=5,blank=True)
    rating=models.FloatField(default=0.0)
    price=models.CharField(max_length=15,blank=True)
    seller_name=models.CharField(max_length=20,blank=True)
    url=models.CharField(max_length=300,blank=True)
    picture_url=models.CharField(max_length=300,blank=True)


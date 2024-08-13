from django.db import models

class Car(models.Model):
    make = models.CharField(max_length=100)
    num_doors = models.CharField(max_length=100, default='4')  # Provide a default value here
    price = models.FloatField()
    description = models.TextField(blank=True)
    body_style = models.CharField(max_length=100)
    engine_type = models.CharField(max_length=100)
    fuel_system = models.CharField(max_length=100)
    wheelbase = models.FloatField()
    length = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()
    curb_weight = models.FloatField()
    fuel_capacity = models.CharField(max_length=100)
    city_mpg = models.IntegerField()
    highway_mpg = models.IntegerField()

    def __str__(self):
        return f'{self.make} {self.num_doors}'

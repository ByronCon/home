import datetime
from django.db import models
from django.utils import timezone

# Master data
class GravityType(models.Model):
    gravity_type_text = models.CharField(max_length=200)

class BottleType(models.Model):
    bottle_type_text = models.CharField(max_length=200)
    bottle_size = models.CharField(max_length=3) #should be different data type

# Transactional data
class Recipe(models.Model):
    # ...
    def __str__(self):
        return self.recipe_text
    recipe_text = models.CharField(max_length=200)
    recipe_ingredients = models.CharField(max_length=200)

class Batch(models.Model):
    # ...
    def __str__(self):
        return self.batch_text

    recipe = models.ForeignKey(Recipe)
    batch_text = models.CharField('Name', max_length=200)
    brew_date = models.DateTimeField('date brewed')

class Measurement(models.Model):
    def __str__(self):
        return self.measurement_date
    batch = models.ForeignKey(Batch)
    measurement_date = models.DateTimeField('date measured')
    gravity_type = models.ForeignKey(GravityType)
    gravity = models.CharField(max_length=4) #should be different data type
    temperature = models.CharField(max_length=3) #should be different data type

class Bottling(models.Model):
    def __str__(self):
        return self.date_bottled

    def was_bottled_recently(self): # bottled in 21 days
        return self.date_bottled >= timezone.now() - datetime.timedelta(days=21)

    batch = models.ForeignKey(Batch)
    measurement = models.ForeignKey(Measurement)
    date_bottled = models.DateTimeField('date bottled')
    bottle_type = models.ForeignKey(BottleType)
    num_bottles = models.IntegerField(default=0)
    markings = models.CharField(max_length=10)
    notes = models.CharField(max_length=200)



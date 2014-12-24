import datetime
from django.db import models
from django.utils import timezone
from django.utils.timezone import localtime

# Master data
class GravityType(models.Model):
    # ...
    # return friendly name
    def __str__(self):
        return self.text

    name = models.CharField(max_length=2)
    description = models.CharField(max_length=200, blank=True)

class BottleType(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True)
    size = models.PositiveIntegerField()

class Ingredient(models.Model):
    # Ingredients for use in a recipe
    name = models.CharField(max_length=100)         # Brewers Sugar
    quantity = models.PositiveIntegerField(default=1)        # 1
    size = models.DecimalField(max_digits=5, decimal_places=2, blank=True)  # 500
    unit = models.CharField(max_length=3)           # g
    cost = models.DecimalField(default=0.00)          # 3.56
    currency = models.CharField(default='AUD')      # AUD

# Transactional data
class Recipe(models.Model):
    # Stores a recipe. Recipe has many ingredients
    def __str__(self):
        return self.text

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True)
    ingredient = models.ManyToManyField(Ingredient)

class Batch(models.Model):
    # What is's all about
    def __str__(self):
        return self.batch_text

    recipe = models.ForeignKey(Recipe)
    name = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=200, blank=True)
    start_date = models.DateTimeField('date brewed')

class Measurement(models.Model):
    def __str__(self):
        return str(localtime(self.measurement_date))

    batch = models.ForeignKey(Batch)
    date = models.DateTimeField('date measured')
    gravity_type = models.ForeignKey(GravityType)
    gravity = models.DecimalField(max_digits=4, decimal_places=3, blank=True)
    temperature = models.IntegerField(blank=True)

class Bottling(models.Model):
    def __str__(self):
        return self.date_bottled

    def was_bottled_recently(self): # bottled in 21 days
        return self.date_bottled >= timezone.now() - datetime.timedelta(days=21)

    batch = models.ForeignKey(Batch)
    final_measurement = models.ForeignKey(Measurement)
    date_bottled = models.DateTimeField('date bottled')
    bottle_type = models.ForeignKey(BottleType)
    num_bottles = models.IntegerField(default=0)
    markings = models.CharField(max_length=10, blank=True)
    notes = models.CharField(max_length=200, blank=True)



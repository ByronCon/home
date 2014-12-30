import datetime
from django.db import models
from django.utils import timezone
from django.utils.timezone import localtime
from django.utils.encoding import force_text

# Master data
class GravityType(models.Model):
    # ...
    # return friendly name
    def __str__(self):
        return self.name

    name = models.CharField(max_length=2)
    description = models.CharField(max_length=200, blank=True, null=True)


class BottleType(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True, null=True)
    size = models.PositiveIntegerField()
    unit = models.CharField(max_length=3)

class Ingredient(models.Model):
    # Ingredients for use in a recipe
    def __str__(self):
        return self.name

    name = models.CharField(max_length=100)                                                         # Brewers Sugar
    quantity = models.PositiveIntegerField(default=1)                                               # 1
    size = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)               # 500
    unit = models.CharField(max_length=3, blank=True, null=True)                                    # g
    cost = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, blank=True, null=True)  # 3.56
    currency = models.CharField(max_length=3, default='AUD', blank=True, null=True)                 # AUD
    # recipe = models.ManyToManyField(Recipe)  # which model should this live in? Who knows. Primary model has access via
    # .<object>.all() while alternate has .<object>_set.all(). Recipe.ingredient_set.all() sounds better than
    # Ingredient.recipe_set.all()  Most likely a user is looking for recipe and finding ingredients, not looking
    # from ingredient to recipe.
    # Arrrgh! Admin implies the opposite.
    # Publication = recipe
    # Article = Ingredient


# Transactional data
class Recipe(models.Model):
    # Stores a recipe. Recipe has many ingredients
    def __str__(self):
        return self.name

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True, null=True)
    ingredient = models.ManyToManyField(Ingredient)  # Refer above


class Batch(models.Model):
    # What it's all about
    def __str__(self):
        if self.name == '':
            friendly = 'Unnamed'
        else:
                friendly = self.name
        friendly = friendly + ' (' + force_text(self.recipe) +  ')'
        return  friendly

    def is_in_fermenter(self):
        # Return if the batch is still sitting in the fermenter.
        return self.bottling_set.count() == 0

    name = models.CharField(max_length=100, blank=True, null=True)
    recipe = models.ForeignKey(Recipe)
    description = models.CharField(max_length=200, blank=True, null=True)
    start_date = models.DateTimeField('date brewed')


class Measurement(models.Model):
    # Reading of temperature and/or gravity
    def __str__(self):
        return str(localtime(self.date))

    batch = models.ForeignKey(Batch)
    date = models.DateTimeField('date measured')
    gravity_type = models.ForeignKey(GravityType)
    gravity = models.DecimalField(max_digits=4, decimal_places=3, blank=True, null=True)
    temperature = models.IntegerField(blank=True, null=True)


class Bottling(models.Model):
    # Bottlings of a batch. May be more than one per batch
    def __str__(self):
        return str(localtime(self.date_bottled))

    def was_bottled_recently(self): # bottled in 21 days
        return self.date_bottled >= timezone.now() - datetime.timedelta(days=21)

    batch = models.ForeignKey(Batch)
    final_measurement = models.ForeignKey(Measurement)
    date_bottled = models.DateTimeField('date bottled')
    bottle_type = models.ForeignKey(BottleType)
    num_bottles = models.IntegerField(default=0)
    markings = models.CharField(max_length=10, blank=True, null=True)
    notes = models.CharField(max_length=200, blank=True, null=True)



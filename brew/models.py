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

    name = models.CharField(max_length=100)  # Brewers Sugar
    quantity = models.PositiveIntegerField(default=1)  # 1
    size = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # 500
    unit = models.CharField(max_length=3, blank=True, null=True)  # g
    cost = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, blank=True, null=True)  # 3.56
    currency = models.CharField(max_length=3, default='AUD', blank=True, null=True)  # AUD


# Transactional data
class Recipe(models.Model):
    # Stores a recipe. Recipe has many ingredients
    def __str__(self):
        return self.name

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True, null=True)
    ingredient = models.ManyToManyField(Ingredient)  # Refer above


class Batch(models.Model):
    class Meta:
        ordering = ['-date']


    # What it's all about
    def __str__(self):
        if self.name == '':
            friendly = 'Unnamed'
        else:
            friendly = self.name
        friendly = friendly + ' (' + force_text(self.recipe) + ')'
        return friendly

    @property
    def age(self):
        " How old is the batch. Only valuable while in fermenter"
        return (timezone.now() - self.date).days + ((timezone.now() - self.date).seconds / 60 / 60 / 24)

    @property
    def is_fermented(self):
        "If FG has been recorded, it's no longer fermenting"
        return self.measurement_set.filter(gravity_type__name="FG").count() > 0

    @property
    def is_bottled(self):
        "Has the beer been bottled yet? Two states; yes & no. May need to introduce a third for partially"
        return self.bottling_set.count() != 0

    @property
    def original_gravity(self):
        return self.measurement_set.filter(gravity_type__name="OG").get().gravity

    @property
    def state(self):
        "What state is the beer in?"
        if self.is_bottled:
            state = "bottled"
        elif self.is_fermented:
            state = "ready to bottle"
        else:
            state = "fermenting"
        return state

    name = models.CharField(max_length=100, blank=True, null=True)
    recipe = models.ForeignKey(Recipe)
    description = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateTimeField('date brewed')


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
        return str(localtime(self.date))

    def was_bottled_recently(self):  # bottled in 21 days
        return self.date >= timezone.now() - datetime.timedelta(days=21)

    @property
    def abv(self):
        "Return ABV % of the bottling"
        return 131 * (self.batch.original_gravity - self.final_measurement.gravity)

    @property
    def days_fermenting(self):
        """ Return days in fermenter """
        age = (self.date - self.batch.date)
        return age.days

    @property
    def age(self):
        """ Return days since bottled """
        return (timezone.now() - self.date).days

    @property
    def all_gone(self):
        """ Are there any beers leftt? """
        return self.num_remaining > 0
        # return false

    @property
    def is_drinkable_in(self):
        """  How many days to go before drinkable (not ready: -ve, ready: +ve) """
        # return self.was_bottled_recently()
        return (timezone.now() - (self.date + datetime.timedelta(days=21))).days

    batch = models.ForeignKey(Batch)
    final_measurement = models.ForeignKey(Measurement)
    date = models.DateTimeField('date bottled')
    bottle_type = models.ForeignKey(BottleType)
    # num_bottles = models.IntegerField(default=0)
    num_bottled = models.IntegerField(default=0)
    num_remaining = models.IntegerField(default=0)
    markings = models.CharField(max_length=10, blank=True, null=True)
    notes = models.CharField(max_length=200, blank=True, null=True)


class Sampling(models.Model):
    """What does the beer taste like"""
    bottling = models.ForeignKey(Bottling)
    date = models.DateTimeField('date sampled')
    rating = models.IntegerField(default=0)
    comment = models.CharField(max_length=200, blank=True, null=True)


#import datetime
#from decimal import Decimal
from django import forms
from django.db import models
from django.db.models import Min, Max
from django.utils import timezone
from datetime import datetime, timedelta
from django.utils.timezone import localtime
from django.utils.encoding import force_text
from django.core.urlresolvers import reverse


# Master data
class GravityType(models.Model):
    # ...
    # return friendly name
    def __str__(self):
        return self.description

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
    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('brew:recipe_detail', kwargs={'pk': self.pk})

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True, null=True)
    ingredient = models.ManyToManyField(Ingredient)  # Refer above
    date = models.DateTimeField('date created', default=datetime.now)
    min_fermentation_days = models.IntegerField('guideline days in fermenter', default=7)
    min_bottled_days = models.IntegerField('min days in bottle', default=14)


class Batch(models.Model):
    # An instance of a recipe.
    class Meta:
        ordering = ['-date']

    def __str__(self):
        if self.name == '':
            friendly = 'Unnamed'
        else:
            friendly = self.name
        friendly = friendly + ' (' + force_text(self.recipe) + ')'
        return friendly

    @property
    def time_fermenting(self):
        """ How long was the batch in primary fermentation? """
        if self.is_bottled:
            end_date = self.bottling_set.aggregate(Min('date'))['date__min']
        else:
            end_date = timezone.now()

        return end_date - self.date

    @property
    def age(self):
        """ How old is the batch. Only valuable while in fermenter"""

        # Add Decimal at the before the open bracket to make it return decimal to many places.
        return (timezone.now() - self.date).days

    @property
    def is_fermented(self):
        """If FG has been recorded, it's no longer fermenting"""
        return self.measurement_set.filter(gravity_type__name="FG").count() > 0

    @property
    def is_bottled(self):
        """Has the beer been bottled yet? Two states; yes & no. May need to introduce a third for partially"""
        return self.bottling_set.count() != 0

    @property
    def original_gravity(self):
        og_measurement = self.measurement_set.filter(gravity_type__name="OG")

        # If OG, return it. Otherwise 0
        if og_measurement:
            return self.measurement_set.filter(gravity_type__name="OG").get().gravity
        else:
            return 0

    @property
    def last_gravity(self):
        """ Return currently known ABV. Use last measurement; regardless of IG/FG """
        max_date = self.measurement_set.aggregate(Max('date'))['date__max']

        if not max_date:
            fg = 0      # if no measurements, FG=0
        else:
            fg = self.measurement_set.filter(date=max_date)[0].gravity

        return fg

    @property
    def bottled_date(self):
        return self.bottling_set.aggregate(Min('date'))['date__min']

    @property
    def state(self):
        """What state is the beer in?"""
        if self.is_bottled:
            state = "bottled"
        elif self.is_fermented:
            state = "ready to bottle"
        else:
            state = "fermenting"
        return state

    @property
    def abv(self):
        """ Return currently known ABV. Use last measurement; regardless of IG/FG """
        # max_date = self.measurement_set.aggregate(Max('date'))['date__max']
        #
        # # if no measurements, return 0.
        # if not max_date:
        #     return 0

        fg = self.last_gravity
        if fg == 0:
            return 0
        else:
            return 131 * (self.original_gravity - fg)

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
    """ Bottlings of a batch. May be more than one per batch """
    class Meta:
        ordering = ['-date']

    def __str__(self):
        return str(localtime(self.date))

    def get_absolute_url(self):
        return reverse('brew:drink_detail', kwargs={'pk': self.pk})

    @property
    def abv(self):
        "Return ABV % of the bottling"
        return 131 * (self.batch.original_gravity - self.final_measurement.gravity)

    @property
    def days_fermenting(self):
        """ Return days in fermenter. Is this useful? """
        age = (self.date - self.batch.date)
        return age.days


    @property
    def secondary_fermentation_date(self):
        """ Return date when the secondary fermentation will be complete. Expected to be used by templates using |timesince.
        """
        expected_time_in_bottle = self.batch.recipe.min_bottled_days
        secondary_date = self.date + timedelta(days=expected_time_in_bottle)
        return secondary_date

    @property
    def secondary_fermentation_complete(self):
        """ Returns a number out of 100 representing how far through bottle time we are. Used primarily for graphs"""
        time_in_bottle = (timezone.now() - self.date).total_seconds()           # convert to seconds
        expected_time_in_bottle = self.batch.recipe.min_bottled_days * 60 * 60 * 24  # convert to seconds
        #return (time_in_bottle / expected_time_in_bottle) * 100
        return 14


    @property
    def age(self):
        """ Return days since bottled """
        return (timezone.now() - self.date).days

    @property
    def all_gone(self):
        """ Are there any beers leftt? """
        return self.num_remaining <= 0

    @property
    def is_drinkable_in(self):
        """  How many days to go before drinkable (not ready: -ve, ready: +ve) """
        # return self.was_bottled_recently()
        return (timezone.now() - (self.date + timedelta(days=14))).days

    batch = models.ForeignKey(Batch)
    final_measurement = models.ForeignKey(Measurement)
    date = models.DateTimeField('date bottled')
    bottle_type = models.ForeignKey(BottleType)
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



### Forms
class RecipeForm(forms.ModelForm):
    """ Represent Recipe's as a form for create/update"""
    class Meta:
        model = Recipe
        exclude = []


class BatchForm(forms.ModelForm):
    """ Form used to update batches """
    class Meta:
        model = Batch
        fields = ['id', 'name', 'recipe', 'description', 'date']
        widgets = {
            'date': forms.TextInput(attrs={'class': 'form_datetime'}),
        }

class MeasurementForm(forms.ModelForm):
    """ Form to update measurements against a batch """
    class Meta:
        model = Measurement
        fields = ['batch', 'date', 'gravity_type', 'gravity', 'temperature']
        widgets = {
            'date': forms.TextInput(attrs={'class': 'form_datetime'}),
        }


class BottlingForm(forms.ModelForm):
    """ Form to create/update bottlings """
    class Meta:
        model = Bottling
        exclude = ['Batch']
        widgets = {
            'date': forms.TextInput(attrs={'class': 'form_datetime'}),
        }
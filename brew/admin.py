from django.contrib import admin

# Register your models here.
from brew.models import Recipe, Batch, Measurement, Bottling, BottleType, GravityType

admin.site.register(Recipe)
admin.site.register(Batch)
admin.site.register(Measurement)
admin.site.register(Bottling)
admin.site.register(BottleType)
admin.site.register(GravityType)
from django.contrib import admin
from brew.models import Recipe, Batch, Measurement, Bottling, BottleType, GravityType, Ingredient, Sampling

# Class definitions


class MeasurementInline(admin.StackedInline):
    # Enable measurement inline for batch modifications
    model = Measurement
    extra = 1


class BatchAdmin(admin.ModelAdmin):
    # list view
    list_display = ('name', 'recipe', 'date')
    sort_field = {'start_date'}

    # detail view
    fieldsets = [
        (None,               {'fields': ['recipe', 'name']}),
        ('Date information', {'fields': ['date'], 'classes': ['collapse']}),
    ]
    inlines = [MeasurementInline]



#class BatchAdmin(admin.ModelAdmin):

# Register your models here.
admin.site.register(Recipe)
admin.site.register(Batch, BatchAdmin)
admin.site.register(Measurement)
admin.site.register(Bottling)
admin.site.register(Ingredient)
admin.site.register(BottleType)
admin.site.register(GravityType)
admin.site.register(Sampling)


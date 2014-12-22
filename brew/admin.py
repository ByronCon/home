from django.contrib import admin
from brew.models import Recipe, Batch, Measurement, Bottling, BottleType, GravityType

# Class definitions

class MeasurementInline(admin.StackedInline):
    # Enable measurement inline for batch modifications
    model = Measurement
    extra = 1

class  BatchAdmin(admin.ModelAdmin):
    #list view
    list_display = ('batch_text', 'recipe', 'brew_date')
    sort_field = {'brew_date'}

    #detail view
    fieldsets = [
        (None,               {'fields': ['recipe', 'batch_text']}),
        ('Date information', {'fields': ['brew_date'], 'classes': ['collapse']}),
    ]
    inlines = [MeasurementInline]



#class BatchAdmin(admin.ModelAdmin):

# Register your models here.
admin.site.register(Recipe)
admin.site.register(Batch, BatchAdmin)
admin.site.register(Measurement)
admin.site.register(Bottling)
admin.site.register(BottleType)
admin.site.register(GravityType)


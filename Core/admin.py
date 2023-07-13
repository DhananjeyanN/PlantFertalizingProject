from django.contrib import admin

from Core.models import Plant, DataTable

# Register your models here.
class DataTableAdmin(admin.ModelAdmin):
    list_display = ('plant', 'm_temp', 'm_moist', 'm_ec', 'm_npk', 'm_ph', 'date_time')
    list_editable = ('m_temp', 'm_moist', 'm_ec', 'm_npk', 'm_ph')
    list_filter = ('plant', 'm_temp', 'm_moist', 'm_ec', 'm_npk', 'm_ph', 'date_time')
    search_fields = ('plant__name', 'm_temp', 'm_moist', 'm_ec', 'm_npk', 'm_ph', 'date_time')

class PlantAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'photo', 'ec', 'ph', 'npk', 'temperature', 'ideal_moisture', 'fertilizer','plant_coefficient')
    list_display_links = ('name',)
    list_editable = ('photo', 'ec', 'ph', 'npk', 'temperature', 'ideal_moisture', 'fertilizer','plant_coefficient')
    list_filter = ( 'name', 'photo', 'ec', 'ph', 'npk', 'temperature', 'ideal_moisture', 'fertilizer','plant_coefficient')
    search_fields = ( 'name', 'photo', 'ec', 'ph', 'npk', 'temperature', 'ideal_moisture', 'fertilizer','plant_coefficient')

admin.site.register(Plant, PlantAdmin)
admin.site.register(DataTable, DataTableAdmin)



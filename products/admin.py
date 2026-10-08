from django.contrib import admin
from .models import Uniform, UniformSize

@admin.register(Uniform)
class UniformAdmin(admin.ModelAdmin):
    list_display = ['name', 'gender', 'price', 'stock']
    list_filter = ['gender', 'created_at']
    search_fields = ['name']

admin.site.register(UniformSize)

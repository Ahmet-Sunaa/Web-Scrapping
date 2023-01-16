from django.contrib import admin
from .models import Products


class ProductsAdmin(admin.ModelAdmin):

    list_display = ('title','brand','model','seller_name')
    list_filter = ('brand','model','seller_name')
    search_fields = ['brand','model','seller_name']
    class Meta:
        model = Products


admin.site.register(Products , ProductsAdmin)

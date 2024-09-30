from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = (
        'productLink', 'sku', 'productName', 'rating', 'stock', 'sales', 'price', 'discount', 'beforeDiscount', 'brand',
        'image',
        'sellerName', 'sellerRating', 'chatRespomse')


@admin.register(Tracking)
class TrackingAdmin(admin.ModelAdmin):
    list_display = ('user','product')

admin.site.register(Profile)
# admin.site.register(Tracking)
# admin.site.register(Tag)

# Register your models here.
from django.contrib import admin

# Register your models here.

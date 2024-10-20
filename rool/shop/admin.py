from django.contrib import admin

from shop.models import CatTransport, Transport

# from accoun.shop.models import Basket

admin.site.register(CatTransport)
admin.site.register(Transport)

# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('name', 'price', 'quantity')
#     fields = ('name', 'description', 'price', 'quantity')
#     readonly_fields = ('description',)
#     search_fields = ('name',)

# class BasketAdmin(admin.ModelAdmin):
#     model = Basket
#     fields = ('product', 'quantity')
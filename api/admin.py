from django.contrib import admin
from .models import Table, Customer, Order, ItemGenre, Item, OrderDetail, Option, OrderedOption, AvailableOption)

# Register your models here.
admin.site.register(Table)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(ItemGenre)
admin.site.register(Item)
admin.site.register(OrderDetail)
admin.site.register(Option)
admin.site.register(OrderedOption)
admin.site.register(AvailableOption)

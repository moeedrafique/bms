from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(CustomUser)
admin.site.register(Branch)
admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(Unit)
admin.site.register(Category)
admin.site.register(Inventory)
admin.site.register(Notification)
admin.site.register(Profile)
admin.site.register(Invitation)
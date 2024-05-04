from django.contrib import admin

# Register your models here.
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import *
from django.contrib.auth.models import Permission

from django.contrib.contenttypes.models import ContentType

@admin.register(ContentType)
@admin.register(Permission)
@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource

admin.site.register(CustomUser)
admin.site.register(Branch)
admin.site.register(Supplier)
admin.site.register(Customer)
admin.site.register(Sale)
admin.site.register(SaleItem)
admin.site.register(Unit)
admin.site.register(Category)
admin.site.register(Inventory)
admin.site.register(Notification)
admin.site.register(Profile)
admin.site.register(Invitation)
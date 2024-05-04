from django.urls import path
from . views import *
from django.contrib.auth import views as auth_views
from .views import PasswordChangeView



urlpatterns = [
    path('', dashboard, name="index"),
    path('suppliers/', all_suppliers, name='all_suppliers'),
    path('supplier/<int:supplier_id>/', supplier_products, name='supplier_products'),
    path('supplier/add', supplier_add, name='supplier_add'),

    path('customers/', all_customer, name='all_customers'),

    path('inventory/stock/', all_inventory, name='all_inventory'),
    path('inventory/stock/adjustment/', inventory_adjust, name='inventory_adjust'),
    path('inventory/add/', inventory_add, name='inventory_add'),
    path('get_product_details/<int:product_id>/', get_product_details, name='get_product_details'),
    path('delete-product/<int:product_id>/', product_delete, name='product_delete'),
    path('products/', all_products, name='all_products'),
    path('products/add', product_add, name='product_add'),
    path('product/edit/<int:product_id>/', product_add_edit, name='product_edit'),

    path('create_sale/', create_sale, name='create_sale'),
    path('administration/users/', manage_user_permissions, name='manage_user_permissions'),

    path('add_unit/', add_unit_view, name='add_unit_view'),
    path('send-invitation/', send_invitation, name='send_invitation'),
    path('get-unit-options/', get_unit_options, name='get_unit_options'),
    path('register/<uuid:invitation_token>/', register, name='register_process'),
    path('registration-success/', registration_success, name='registration_success'),
    path('invalid-invitation/', invalid_invitation, name='invalid_invitation'),
    path('top-selling-products/', top_selling_products, name='top_selling_products'),
    path('sales-chart-data/', sales_chart_data, name='sales_chart_data'),
    path('save_sale/', save_sale, name='save_sale'),

]

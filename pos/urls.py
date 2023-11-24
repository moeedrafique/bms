from django.urls import path
from . views import *
from django.contrib.auth import views as auth_views
from .views import PasswordChangeView

urlpatterns = [
    path('', dashboard, name="index"),
    path('products/', all_products, name='all_product'),
    path('product/add/', product_add, name='product_add'),
    path('delete-product/<int:product_id>/', product_delete, name='product_delete'),
    path('add_unit/', add_unit_view, name='add_unit_view'),
    path('send-invitation/', send_invitation, name='send_invitation'),
    path('get-unit-options/', get_unit_options, name='get_unit_options'),
    path('register/<uuid:invitation_token>/', register, name='register_process'),
    path('registration-success/', registration_success, name='registration_success'),
    path('invalid-invitation/', invalid_invitation, name='invalid_invitation'),

]

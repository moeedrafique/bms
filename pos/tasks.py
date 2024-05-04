from celery import shared_task
from datetime import date

from django.contrib.auth.models import User
from django.utils import timezone

from .models import *


@shared_task
def check_product_expiry(product_id):
    product = Inventory.objects.get(id=product_id)
    if product.expiry_date and product.expiry_date <= timezone.now().date():
        user = User.objects.first()  # Replace with your actual user or user selection logic
        message = f"The product {product.name} has expired."
        category = 'expired_product'
        Notification.objects.create(user=user, message=message, category=category)


@shared_task
def notify_five_days_before_expiry(product_id):
    product = Inventory.objects.get(id=product_id)
    expiry_in_five_days = product.expiry_date - timezone.timedelta(days=5)

    if timezone.now().date() == expiry_in_five_days:
        user = User.objects.first()  # Replace with your actual user or user selection logic
        message = f"The product {product.name} will expire in 5 days."
        category = 'five_days_before_expiry'
        Notification.objects.create(user=user, message=message, category=category)
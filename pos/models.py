import uuid

from celery import chain
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.db.models.signals import post_save
# Create your models here.
from django.dispatch import receiver
from django.urls import reverse

from .tasks import check_product_expiry, notify_five_days_before_expiry
from django.utils import timezone


class Branch(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile_user')
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    # Add other fields as needed

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile_user.save()

ROLE_CHOICES = (
    (1, "Admin"),
    (2, "Manager"),
    (3, "Storekeeper"),
    (4, "Staff"),
)

class CustomUser(AbstractUser):
    user_type = models.IntegerField(choices=ROLE_CHOICES, blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True, blank=True, related_name='custom_user_profile')


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Unit(models.Model):
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    UNIT_CHOICES = [
        ('carton', 'Carton'),
        ('gallon', 'Gallon'),
        ('packs', 'Packs'),
        # Add more choices as needed
    ]
    batch_number = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    quantity = models.IntegerField(null=True)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, blank=True, null=True)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    expiry_date = models.DateField(null=True, blank=True)
    reorder_level = models.IntegerField(default=10)
    overstock_level = models.IntegerField(default=100)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='products', blank=True, null=True)
    note = models.TextField(null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Inventory(models.Model):
    quantity = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventory')
    transaction_type = models.CharField(max_length=20)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} units"


class Notification(models.Model):
    # auth_user_id = models.OneToOneField(CustomUser,on_delete=models.CASCADE, null=True)
    message = models.TextField()
    category = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.message} ({self.category})"


@receiver(post_save, sender=Product)
def check_and_notify_expiry(sender, instance, **kwargs):
    if instance.expiry_date and instance.expiry_date <= timezone.now().date():
        # Trigger the Celery task to check product expiry
        chain(check_product_expiry.si(instance.id))()

    # Trigger the Celery task to notify 5 days before expiry
    expiry_check_date = instance.expiry_date - timezone.timedelta(days=5)
    if timezone.now().date() == expiry_check_date:
        chain(notify_five_days_before_expiry.si(instance.id))()


class Invitation(models.Model):
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='sent_invitations')
    recipient_email = models.EmailField()
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='invitation', blank=True, null=True)
    role = models.IntegerField(choices=ROLE_CHOICES) # Add role field
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_accepted = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('register_process', kwargs={'invitation_token': self.token})
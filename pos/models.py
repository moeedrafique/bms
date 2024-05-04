import random
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
from import_export import resources

from .tasks import check_product_expiry, notify_five_days_before_expiry
from django.utils import timezone


class Branch(models.Model):
    BRANCH_TYPE_CHOICES = [
        ('Warehouse', 'Warehouse'),
        ('Branch', 'Branch'),
    ]

    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    branch_type = models.CharField(max_length=10, choices=BRANCH_TYPE_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.branch_type})"

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile_user')
    passport = models.CharField(max_length=100, null=True, blank=True)
    uid_no = models.CharField(max_length=100, null=True, blank=True)
    date_started = models.DateField(null=True, blank=True)
    permit_granted_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
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
    (2, "Store Manager"),
    (3, "Staff"),
)

class CustomUser(AbstractUser):
    user_type = models.IntegerField(choices=ROLE_CHOICES, blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True, blank=True, related_name='custom_user_profile')


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    brn = models.CharField(max_length=255, blank=True, null=True)
    vat = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
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

class Inventory(models.Model):
    UNIT_CHOICES = [
        ('carton', 'Carton'),
        ('gallon', 'Gallon'),
        ('packs', 'Packs'),
        # Add more choices as needed
    ]
    batch_number = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=255, default=None, null=True, blank=True)
    description = models.TextField(default=None, null=True, blank=True)
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
        return f"{self.name} - {self.quantity} units"

class StockAdjustment(models.Model):
    date = models.DateField()
    reference_no = models.CharField(max_length=6, unique=True)
    note = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.reference_no:
            self.reference_no = self._generate_reference_no()
        super().save(*args, **kwargs)

    def _generate_reference_no(self):
        """
        Generate a 6-digit random reference number.
        """
        return str(random.randint(100000, 999999))

    def __str__(self):
        return f"Stock Adjustment - {self.reference_no}"

class Product(models.Model):
    name = models.CharField(max_length=255)
    # description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    # image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        exclude = ('created_at', 'updated_at', 'image')

class Customer(models.Model):
    name = models.CharField(max_length=255)
    # Add other fields as needed

    def __str__(self):
        return self.name

class Sale(models.Model):
    PENDING = 'Pending'
    PAID = 'Paid'
    DEPOSITED = 'Deposited'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PAID, 'Paid'),
        (DEPOSITED, 'Deposited'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, blank=True, null=True)
    products = models.ManyToManyField('Product', through='SaleItem')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    arrival_date = models.DateField(blank=True, null=True)  # New field for customer arrival date
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Sale #{self.id}"


    def calculate_total_amount(self):
        total = 0
        sale_items = SaleItem.objects.filter(sale=self)
        for item in sale_items:
            total += item.calculate_item_total()
        return total

@receiver(post_save, sender=Sale)
def send_arrival_notification(sender, instance, **kwargs):
    if instance.arrival_date == timezone.now().date():
        # Create a Notification instance to record the event
        Notification.objects.create(
            message=f"Customer {instance.customer} will arrive today.",
            category="Customer Arrival"
        )

# models.py
class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def calculate_item_total(self):
        return self.quantity * self.unit_price

class Notification(models.Model):
    # auth_user_id = models.OneToOneField(CustomUser,on_delete=models.CASCADE, null=True)
    message = models.TextField()
    category = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.message} ({self.category})"


@receiver(post_save, sender=Inventory)
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
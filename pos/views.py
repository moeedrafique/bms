import json
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import permission_required, user_passes_test, login_required
from django.contrib.auth.models import Permission
from django.contrib.auth.views import PasswordChangeView
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import Sum
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from .forms import ProductForm, UnitForm, InvitationForm, CustomUserCreationForm, SaleForm, SupplierForm
from .models import *

# @login_required
def manage_user_permissions(request):
    # if not request.user.is_superuser:
    #     return redirect('home')  # Redirect non-admins to home page

    users = CustomUser.objects.all()

    # Assuming you have models named Product and Order
    product_content_type = ContentType.objects.get_for_model(Product)
    order_content_type = ContentType.objects.get_for_model(Sale)

    product_permissions = Permission.objects.filter(content_type=product_content_type)
    order_permissions = Permission.objects.filter(content_type=order_content_type)

    if request.method == 'POST':
        # Handle form submission to assign/revoke permissions
        selected_user_id = request.POST.get('user_id')
        selected_user = CustomUser.objects.get(id=selected_user_id)
        selected_product_permission_ids = request.POST.getlist('product_permissions')
        selected_order_permission_ids = request.POST.getlist('order_permissions')

        # Assign selected product permissions to the user
        selected_user.user_permissions.add(*selected_product_permission_ids)
        # Assign selected order permissions to the user
        selected_user.user_permissions.add(*selected_order_permission_ids)

        return redirect('manage_user_permissions')

    return render(request, 'users.html', {
        'users': users,
        'product_permissions': product_permissions,
        'order_permissions': order_permissions
    })

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

@login_required(login_url='account_login')
@require_http_methods(["GET"])
def dashboard(request):
    branches = Branch.objects.all()
    # Check if it's an Ajax request
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        selected_branch_id = request.GET.get('branch', None)
        if selected_branch_id:
            selected_branch = Branch.objects.get(pk=selected_branch_id)
            products = Inventory.objects.filter(branch=selected_branch)
            inventory = Inventory.objects.filter(product__branch=selected_branch)
        else:
            selected_branch = None
            products = Inventory.objects.all()
            inventory = Inventory.objects.all()

        product_data = [{'name': product.name, 'unit': product.unit} for product in products]
        print(product_data)
        inventory_data = [{'name': item.product.name, 'quantity': item.quantity, 'transaction_type': item.transaction_type} for item in inventory]

        return JsonResponse({'products': product_data, 'inventory': inventory_data, 'selected_branch': selected_branch.name if selected_branch else None})

    return render(request, 'index.html', {'branches': branches})

@login_required(login_url='account_login')
def all_customer(request):
    customer = Customer.objects.all()
    context = {'customer': customer}
    return render(request, 'all_customers.html', context)

@login_required(login_url='account_login')
def all_suppliers(request):
    supplier = Supplier.objects.all()
    context = {'supplier': supplier}
    return render(request, 'all_suppliers.html', context)

def supplier_products(request, supplier_id):
    supplier = get_object_or_404(Supplier, pk=supplier_id)
    products = Inventory.objects.filter(supplier=supplier)
    context = {
        'supplier': supplier,
        'products': products
    }
    return render(request, 'supplier_products.html', context)

@login_required(login_url='account_login')
def supplier_add(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save()
            return JsonResponse({'success': True, 'supplier_name': supplier.name})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = SupplierForm()
    return render(request, 'add_supplier.html', {'form': form})

@login_required(login_url='account_login')
def all_inventory(request):
    product = Inventory.objects.all()
    context = {'product': product}
    return render(request, 'all_inventory.html', context)

@login_required(login_url='account_login')
def inventory_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            return JsonResponse({'success': True, 'product_name': product.name, 'product_unit': product.unit.name})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

@login_required(login_url='account_login')
def inventory_adjust(request):
    product = Inventory.objects.all()
    context = {'product': product}
    return render(request, 'inventory_adjustment.html', context)

def get_product_details(request, product_id):
    try:
        product = Inventory.objects.get(pk=product_id)
        data = {
            'name': product.name,
            'stock': product.quantity
        }
        return JsonResponse(data)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

@login_required(login_url='account_login')
def all_products(request):
    product = Product.objects.all()
    context = {'product': product}
    return render(request, 'all_product.html', context)


# @login_required(login_url='account_login')
@permission_required('pos.add_product', raise_exception=True)
def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            return JsonResponse({'success': True, 'product_name': product.name, 'product_unit': product.unit.name})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

# Add a handler for PermissionDenied exception to show a message for users without permission
def permission_denied_handler(request, exception):
    messages.error(request, "You don't have permission to add a product.")
    return redirect('index')  # Redirect to the home page or any other appropriate page

@login_required(login_url='account_login')
def product_add_edit(request, product_id=None):
    # If product_id is provided, it's an edit request
    if product_id:
        product = get_object_or_404(Product, id=product_id)
        form = ProductForm(request.POST or None, instance=product)
    else:
        form = ProductForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            product = form.save()
            return JsonResponse({'success': True, 'product_name': product.name, 'product_unit': product.unit.name})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

    return render(request, 'add_product.html', {'form': form})

# Delete Currency
@login_required(login_url='account_login')
def product_delete(request, product_id):
    # Get the product object or return a 404 response if not found
    product = get_object_or_404(Inventory, id=product_id)

    # Perform the delete operation
    product.delete()

    # Return a JSON response indicating success
    return JsonResponse({'success': True})

@csrf_exempt  # Use csrf_exempt for simplicity in this example. Consider using CSRF protection in production.
def add_unit_view(request):
    if request.method == 'POST':
        # Assuming you have a form for adding units
        form = UnitForm(request.POST)
        if form.is_valid():
            # Process the form data and add the unit to the database

            # Assuming you have a Unit model and you just created a unit
            unit = Unit.objects.create(name=form.cleaned_data['name'])

            return JsonResponse({'success': True, 'unit_id': unit.id, 'unit_name': unit.name})
        else:
            errors = form.errors
            return JsonResponse({'success': False, 'errors': errors})

    # Handle other HTTP methods if needed
    return JsonResponse({'success': False, 'errors': 'Invalid request method'})

def get_unit_options(request):
    units = Unit.objects.all()
    options = [{'id': unit.id, 'name': unit.name} for unit in units]
    return JsonResponse({'options': options})




@login_required(login_url='account_login')
def create_sale(request):
    products = Product.objects.all()
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            # Create a new sale
            sale = Sale.objects.create(
                user=request.user,
                branch=form.cleaned_data['branch'],
                customer=form.cleaned_data['customer']
            )

            # Add selected products to the sale
            for product in form.cleaned_data['products']:
                SaleItem.objects.create(
                    sale=sale,
                    product=product,
                    quantity=1,  # You may customize this based on your needs
                    unit_price=product.price  # Assuming the product has a 'price' field
                )

            # Calculate the total amount for the sale
            sale.total_amount = sum(item.calculate_item_total() for item in sale.saleitem_set.all())
            sale.save()

            return redirect('sales_list')  # Redirect to a sales list or confirmation page
    else:
        form = SaleForm()

    return render(request, 'create_sales.html', {'form': form, 'products':products})


@transaction.atomic
@csrf_exempt  # Disable CSRF protection for simplicity (use a decorator with proper validation in production)
def save_sale(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            branch_id = data.get('branch_id')
            customer_id = data.get('customer_id')
            total = data.get('total')
            deposit = data.get('deposit')
            discount = data.get('discount')
            products = data.get('products', [])

            print(discount)
            print(products)

            # Add sale items
            for product in products:
                product_id = product.get('id')
                quantity = product.get('quantity')
                unit_price = product.get('subtotal')
                print(unit_price)

                # Validate that product_id and quantity_sold are provided
                if not product_id or not quantity:
                    raise ValueError('Product ID and Quantity are required.')


                product = Product.objects.get(pk=product_id)

                # Check if there is enough quantity to sell
                if product.quantity < quantity:
                    raise ValueError('Insufficient quantity in stock.')


                # Create a new sale
                sale = Sale.objects.create(user_id=user_id, branch_id=branch_id, customer_id=customer_id)

                SaleItem.objects.create(sale=sale, product_id=product_id, quantity=quantity, unit_price=unit_price)

                # Update Product quantity
                product.quantity -= quantity
                product.save()

            # Update total_amount in the sale model (you might need to adjust this based on your logic)
            sale.total_amount = total
            sale.discount = discount
            sale.remaining_amount = deposit
            sale.save()

            # Render the receipt template with sale data
            receipt_html = render(request, 'reciept.html', {'sale': sale})
            receipt_html_str = receipt_html.content.decode('utf-8')  # Convert bytes to string

            return render(request, 'reciept.html', {'sale': sale})

        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Product not found.'})

        except ValueError as e:
            return JsonResponse({'success': False, 'message': str(e)})
        #
        # except Exception as e:
        #     return JsonResponse({'success': False, 'message': 'An error occurred. Please try again.'})

def is_admin(user):
    return user.user_type == 'admin'

# @user_passes_test(is_admin, login_url='account_login')
# @permission_required('pos.can_send_invitation', login_url='account_login')
@login_required(login_url='account_login')
def send_invitation(request):
    if request.method == 'POST':
        form = InvitationForm(request.POST)
        if form.is_valid():
            invitation = form.save(commit=False)
            invitation.sender = request.user
            invitation.save()

            print(invitation.token)
            # Send invitation email and other logic
            # Send invitation email
            subject = 'Invitation to join our site'
            message = render_to_string('email/invitation_email.txt', {'invitation': invitation})
            html_message = render_to_string('email/invitation_email.html', {'invitation': invitation})
            from_email = 'alimoeed15@gmail.com'  # Set your from email address
            to_email = invitation.recipient_email

            send_mail(
                subject,
                strip_tags(message),
                from_email,
                [to_email],
                html_message=html_message,
            )

            messages.success(request, f'Invitation sent to {invitation.recipient_email}.')
            return redirect('index')
    else:
        form = InvitationForm()

    return render(request, 'send_invitation.html', {'form': form})


def get_invitation_by_token(token):
    try:
        invitation = Invitation.objects.get(token=token)
        return invitation
    except Invitation.DoesNotExist:
        return None


def register(request, invitation_token):
    invitation = get_invitation_by_token(invitation_token)

    # Check if the invitation is invalid or has already been accepted
    if not invitation or invitation.is_accepted:
        return redirect('invalid_invitation')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = invitation.role
            user.branch = invitation.branch
            user.save()
            # Additional logic to associate the user with the invitation
            invitation.is_accepted = True
            invitation.user = user
            invitation.save()
            # Log in the user
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})

def registration_success(request):
    return render(request, 'invalid_invitation.html')


def invalid_invitation(request):
    return render(request, 'invalid_invitation.html')

def handler404(request, exception):
    return render(request, 'comm/404.htm')


def handler500(request):
    return render(request, 'comm/500.htm')


# VISUALIZATIOn
def top_selling_products(request):
    # Aggregate sales items to calculate total quantity sold for each product
    top_selling = SaleItem.objects.values('product__name').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:5]

    top_selling_data = {
        'labels': [item['product__name'] for item in top_selling],
        'data': [item['total_quantity'] for item in top_selling],
    }

    return JsonResponse(top_selling_data)


@require_GET
def sales_chart_data(request):
    time_range = request.GET.get('time_range', 'this_week')

    today = timezone.now().date()

    if time_range == 'this_week':
        start_date = today - timedelta(days=today.weekday())
        end_date = today + timedelta(days=(6 - today.weekday()))
    elif time_range == 'last_week':
        start_date = today - timedelta(days=today.weekday() + 7)
        end_date = today - timedelta(days=today.weekday() + 1)
    elif time_range == 'this_month':
        start_date = today.replace(day=1)
        end_date = today.replace(day=timezone.now().monthrange(today.year, today.month)[1])
    elif time_range == 'last_month':
        start_date = today.replace(day=1) - timedelta(days=1)
        end_date = start_date.replace(day=timezone.now().monthrange(start_date.year, start_date.month)[1])
    elif time_range == 'this_year':
        start_date = today.replace(month=1, day=1)
        end_date = today.replace(month=12, day=31)
    elif time_range == 'last_year':
        start_date = today.replace(year=today.year - 1, month=1, day=1)
        end_date = today.replace(year=today.year - 1, month=12, day=31)
    else:
        return JsonResponse({'error': 'Invalid time range'}, status=400)

    sales_data = Sale.objects.filter(created_at__range=[start_date, end_date]). \
        values('created_at__date').annotate(total_amount=Sum('total_amount'))

    labels = [entry['created_at__date'] for entry in sales_data]
    data = [entry['total_amount'] for entry in sales_data]

    return JsonResponse({'labels': labels, 'data': data})
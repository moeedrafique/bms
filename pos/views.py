from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import permission_required, user_passes_test
from django.contrib.auth.views import PasswordChangeView
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from .forms import ProductForm, UnitForm, InvitationForm, CustomUserCreationForm
from .models import *

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

@require_http_methods(["GET"])
def dashboard(request):
    branches = Branch.objects.all()
    # Check if it's an Ajax request
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        selected_branch_id = request.GET.get('branch', None)
        if selected_branch_id:
            selected_branch = Branch.objects.get(pk=selected_branch_id)
            products = Product.objects.filter(branch=selected_branch)
            inventory = Inventory.objects.filter(product__branch=selected_branch)
        else:
            selected_branch = None
            products = Product.objects.all()
            inventory = Inventory.objects.all()

        product_data = [{'name': product.name, 'unit': product.unit} for product in products]
        print(product_data)
        inventory_data = [{'name': item.product.name, 'quantity': item.quantity, 'transaction_type': item.transaction_type} for item in inventory]

        return JsonResponse({'products': product_data, 'inventory': inventory_data, 'selected_branch': selected_branch.name if selected_branch else None})

    return render(request, 'index.html', {'branches': branches})

def all_products(request):
    product = Product.objects.all()
    context = {'product': product}
    return render(request, 'all_product.html', context)

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

# Delete Currency
def product_delete(request, product_id):
    # Get the product object or return a 404 response if not found
    product = get_object_or_404(Product, id=product_id)

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


def is_admin(user):
    return user.user_type == 'admin'

# @user_passes_test(is_admin, login_url='account_login')
# @permission_required('pos.can_send_invitation', login_url='account_login')
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

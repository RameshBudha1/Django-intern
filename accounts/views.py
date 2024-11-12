from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . forms import LoginForm
from django.contrib.auth.decorators import login_required
from .auth import admin_only
from userpage.models import Order
from products.models import Products, Category
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta

# to register the user
def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,'Account created successfully')
            return redirect('/account/login')
        else:
            messages.add_message(request,messages.ERROR,'Please verify the form fields')
            return render(request, 'accounts/register.html',{'form':form})
    context = {
        'form': UserCreationForm
    }
    return render(request,'accounts/register.html',context)

# to login the user
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username = data['username'], password = data['password'])
            if user is not None:
                login(request,user)
                return redirect("/account/dashboard")
            else:
                messages.add_message(request, messages.ERROR, "Please provide the correct credentials!")
                return render(request,"accounts/login.html",{'form':form})
    context = {
        'form': LoginForm
    }
    return render(request,'accounts/login.html',context)

def user_logout(request):
    logout(request)
    return redirect('/')

@login_required
@admin_only
def dashboard(request):
    # Get counts and statistics
    total_orders = Order.objects.count()
    total_users = User.objects.count()
    total_products = Products.objects.count()
    total_admins = User.objects.filter(is_staff=True).count()
    total_categories = Category.objects.count()
    
    # Calculate total revenue
    total_revenue = Order.objects.aggregate(
        total=Sum('total_price')
    )['total'] or 0
    
    # Calculate monthly growth
    last_month = timezone.now() - timedelta(days=30)
    
    # Orders growth
    previous_orders = Order.objects.filter(order_date__lt=last_month).count()
    current_orders = Order.objects.filter(order_date__gte=last_month).count()
    orders_growth = calculate_growth(current_orders, previous_orders)
    
    # Users growth
    previous_users = User.objects.filter(date_joined__lt=last_month).count()
    current_users = User.objects.filter(date_joined__gte=last_month).count()
    users_growth = calculate_growth(current_users, previous_users)
    
    # Products growth
    previous_products = Products.objects.filter(created_at__lt=last_month).count()
    current_products = Products.objects.filter(created_at__gte=last_month).count()
    products_growth = calculate_growth(current_products, previous_products)
    
    # Revenue growth
    previous_revenue = Order.objects.filter(order_date__lt=last_month).aggregate(
        total=Sum('total_price')
    )['total'] or 0
    current_revenue = Order.objects.filter(order_date__gte=last_month).aggregate(
        total=Sum('total_price')
    )['total'] or 0
    revenue_growth = calculate_growth(current_revenue, previous_revenue)
    
    context = {
        'total_orders': total_orders,
        'total_users': total_users,
        'total_products': total_products,
        'total_revenue': total_revenue,
        'total_admins': total_admins,
        'total_categories': total_categories,
        'orders_growth': orders_growth,
        'users_growth': users_growth,
        'products_growth': products_growth,
        'revenue_growth': revenue_growth,
    }
    
    return render(request, "accounts/dashboard.html", context)

def calculate_growth(current, previous):
    if previous == 0:
        return 0
    return ((current - previous) / previous) * 100

from django.shortcuts import render, redirect
from .models import Products, Category
from .forms import CategoryForm, ProductForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.auth import admin_only
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Sum
from userpage.models import Order

# Create your views here.


# function to show products
@login_required
@admin_only
def show_products(request):
    products = Products.objects.all()
    context = {"products": products}
    return render(request, "products/product-list.html", context)


# function to show category
@login_required
@admin_only
def show_category(request):
    categories = Category.objects.all()
    context = {"categories": categories}
    return render(request, "products/category-list.html", context)


# function to add category using form
@login_required
@admin_only
def post_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(
                request, messages.SUCCESS, "Category added successfully!"
            )
            return redirect("/admin/category")
        else:
            messages.add_message(request, messages.ERROR, "Failed to add Category!")
            return render(request, "products/addCategory.html", {"form": CategoryForm})

    context = {"form": CategoryForm}
    return render(request, "products/addCategory.html", context)


# function to add product using form
@login_required
@admin_only
def post_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(
                request, messages.SUCCESS, "Product added successfully!"
            )
            return redirect("/admin/product/")
        else:
            messages.add_message(
                request,
                messages.ERROR,
                "Failed to add product, please verify the form field",
            )
            return render(request, "products/addProduct.html", {"form": ProductForm})
    context = {"form": ProductForm}
    return render(request, "products/addProduct.html", context)


# to delete the category
@login_required
@admin_only

def delete_category(request, category_id):
    category = Category.objects.get(id=category_id)
    category.delete()
    messages.add_message(request, messages.SUCCESS, "Category deleted successfully")
    return redirect("/admin/category")


# to update the category using category form
@login_required
@admin_only
def update_category(request, category_id):
    category = Category.objects.get(id=category_id)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.add_message(
                request, messages.SUCCESS, "Category updated successfully!"
            )
            return redirect("/admin/category")
        else:
            messages.add_message(request, messages.ERROR, "Failed to update category!")
            return render(request, "products/updateCategory.html", {"form": form})
    context = {"form": CategoryForm(instance=category)}
    return render(request, "products/updateCategory.html", context)


# to delete the product
@login_required
@admin_only

def delete_product(request, product_id):
    products = Products.objects.get(id=product_id)
    products.delete()
    messages.add_message(request, messages.SUCCESS, "Product deleted successfully")
    return redirect("/admin/product/")


# to update product using productForm
@login_required
@admin_only

def update_product(request, product_id):
    product = Products.objects.get(id=product_id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.add_message(
                request, messages.SUCCESS, "Product updated successfully"
            )
            return redirect("/admin/product/")
        else:
            messages.add_message(request, messages.ERROR, "Failed to update products")
            return render(request, "products/updateProduct.html", {"form": form})
    context = {"form": ProductForm(instance=product)}
    return render(request, "products/updateProduct.html", context)

@login_required
@admin_only
def show_orders(request):
    # Get all orders with related data
    orders = Order.objects.select_related('user', 'products').all().order_by('-order_date')
    
    # Date range filtering
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        orders = orders.filter(order_date__range=[start_date, end_date])
    
    # Status and payment filtering
    status = request.GET.get('status')
    payment_method = request.GET.get('payment_method')
    
    if status:
        orders = orders.filter(status=status)
    if payment_method:
        orders = orders.filter(payment_method=payment_method)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        orders = orders.filter(
            Q(id__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(contact_no__icontains=search_query) |
            Q(status__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(orders, 10)
    page = request.GET.get('page')
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)
    
    context = {
        'orders': orders,
        'search_query': search_query,
        'start_date': start_date,
        'end_date': end_date,
        'status': status,
        'payment_method': payment_method,
        'payment_choices': Order.PAYMENT,
        'total_orders': orders.paginator.count,
        'total_amount': orders.object_list.aggregate(Sum('total_price'))['total_price__sum'] or 0,
    }
    
    return render(request, "products/order-list.html", context)


@login_required
@admin_only
def order_detail(request, order_id):
    try:
        order = Order.objects.select_related('user', 'products').get(id=order_id)
        
        context = {
            'order': order,
            'payment_choices': Order.PAYMENT,
        }
        
        if request.method == 'POST':
            new_status = request.POST.get('status')
            if new_status:
                order.status = new_status
                order.save()
                messages.success(request, 'Order status updated successfully')
                return redirect('order_detail', order_id=order.id)
                
        return render(request, "products/order.html", context)
        
    except Order.DoesNotExist:
        messages.error(request, 'Order not found')
        return redirect('orders')

@login_required
@admin_only
def update_order(request):
    return render(request, "products/order-edit.html")
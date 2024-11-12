from django.shortcuts import render, redirect
from .models import Products, Category
from .forms import CategoryForm, ProductForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.auth import admin_only

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

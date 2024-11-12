import django_filters
from products.models import Products
from django import forms
from django_filters import CharFilter

class ProductFilter(django_filters.FilterSet):
    productname_contains = CharFilter(
        field_name='product_name',
        lookup_expr='icontains',
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search products...'})
    )

    class Meta:
        model = Products
        fields = []
        exclude = ['product_price', 'product_image', 'product_description', 'product_quantity', 'created_at', 'category']
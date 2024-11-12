from django import forms
from .models import Products, Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category description',
                'rows': 3
            })
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        exclude = ('created_at',)
        widgets = {
            'product_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product name'
            }),
            'product_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter price',
                'min': '0'
            }),
            'product_quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter quantity',
                'min': '0'
            }),
            'product_description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product description',
                'rows': 4
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'product_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }

    def clean_product_price(self):
        price = self.cleaned_data.get('product_price')
        if price and price <= 0:
            raise forms.ValidationError("Price must be greater than zero")
        return price

    def clean_product_quantity(self):
        quantity = self.cleaned_data.get('product_quantity')
        if quantity and quantity < 0:
            raise forms.ValidationError("Quantity cannot be negative")
        return quantity

    def clean_product_image(self):
        image = self.cleaned_data.get('product_image')
        if image:
            if not image.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                raise forms.ValidationError("Only image files (PNG, JPG, JPEG, GIF) are allowed")
        return image
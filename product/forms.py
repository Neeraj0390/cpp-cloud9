from .models import Product
from django import forms

class ProductCreationForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("product_name", "total_quantity", "product_type", 
                  "product_image", "quantity_sold", "selling_price", "buying_price")
        exclude = ('stock_updated_time',)

    def clean_product_name(self):
        name = self.cleaned_data.get('product_name')
        if not name:
            raise forms.ValidationError('This field is required')

        # Check for duplicate product name
        if Product.objects.filter(product_name=name).exists():
            raise forms.ValidationError(f'{name} is already created')

        return name
    

class ProductupdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("product_name", "total_quantity", "product_type", 
                  "product_image", "quantity_sold", "selling_price", "buying_price")

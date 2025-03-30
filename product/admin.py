from django.contrib import admin
from .forms import ProductCreationForm

# Register your models here.
from .models import Product




class ProductCreateAdmin(admin.ModelAdmin):
    list_display=['product_name','product_type','product_image']
    form=ProductCreationForm
    search_fields=['product_type']
    list_filter=["product_type"]
    
admin.site.register(Product, ProductCreateAdmin)    
    
    
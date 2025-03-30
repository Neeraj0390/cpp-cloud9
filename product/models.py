from django.db import models

# Create your models here.
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('ELECTRONICS', 'Electronics'),
        ('GROCERY', 'Grocery'),
        ('FASHION', 'Fashion'),
        ('FURNITURE', 'Furniture'),
    ]
     
    product_name=models.CharField(max_length=50)
    total_quantity=models.IntegerField(null=True)
    product_type=models.CharField(max_length=20,choices=CATEGORY_CHOICES,default='GROCERY')
    stock_updated_time=models.DateTimeField(auto_now=True)
    product_image=models.ImageField(upload_to='product_images/')
    quantity_sold=models.IntegerField(default=0)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    buying_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)


    
    def __str__(self):
      return self.product_name
 
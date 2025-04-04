# Generated by Django 5.1.6 on 2025-02-18 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=50)),
                ('total_quantity', models.IntegerField()),
                ('product_type', models.CharField(choices=[('ELECTRONICS', 'Electronics'), ('GROCERY', 'Grocery'), ('FASHION', 'Fashion'), ('FURNITURE', 'Furniture')], default='GROCERY', max_length=20)),
                ('present_quantity', models.IntegerField(null=True)),
                ('stock_updated_time', models.DateTimeField()),
                ('product_image', models.ImageField(upload_to='product_images/')),
                ('quantity_sold', models.IntegerField(default=0)),
                ('selling_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('buying_price', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
            ],
        ),
    ]

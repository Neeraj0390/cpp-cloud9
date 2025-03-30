# Create your views here.

from django.shortcuts import get_object_or_404, render,redirect
from .models import Product
from django.http import HttpResponse
from .forms import ProductCreationForm,ProductupdateForm
from django.contrib.auth.decorators import login_required,user_passes_test



def listproducts(request):
    # Get the search term from the URL query parameters, defaulting to an empty string if not present
    search_term = request.GET.get('search_term', '')

    # Filter products if there's a search term
    if search_term:
        queryset = Product.objects.filter(product_name__icontains=search_term)
    else:
        queryset = Product.objects.all()

    # Prepare context with the filtered queryset
    context = {
        'product': queryset,
        'search_term': search_term,  # Pass the search term back to the template
    }

    return render(request, "product/home.html", context)




@login_required
@user_passes_test(lambda user:user.is_staff)
def addproducts(request):
    if request.method == 'POST':  # If the form is submitted
        form = ProductCreationForm(request.POST, request.FILES)  # Handle form data and file uploads
        if form.is_valid():
            form.save()  # Save the new product to the database
            return redirect('listprod')  # Redirect to a success page or product list page after saving
    else:
        form = ProductCreationForm()  # Create an empty form for GET request
    
    return render(request, 'product/addprod.html', {'form': form})



@login_required
@user_passes_test(lambda user:user.is_staff)
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        product.delete()
        return redirect('listprod')  # Redirect to product list after deletion
    
    return redirect('listprod')  # If the method is not POST, just redirect to product list


from django.shortcuts import get_object_or_404, render, redirect
from .models import Product
from .forms import ProductupdateForm

@login_required
@user_passes_test(lambda user:user.is_staff)
def update_product(request, product_id):
    # Retrieve the Product object with the given pk (primary key)
    product = get_object_or_404(Product, id=product_id)
    
    # Initialize the form with the product instance (GET request)
    if request.method == 'POST':
        # If the form is submitted, include POST data and files (for file upload)
        form = ProductupdateForm(request.POST, request.FILES, instance=product)
        
        if form.is_valid():
            form.save()  # Save the updated product data
            return redirect('listprod')  # Or use your product list URL (e.g., 'listprod')
    else:
        # For GET request, just load the existing product data into the form
        form = ProductupdateForm(instance=product)

    # Make sure to return the context after both GET and POST requests
    context = {
        'form': form
    }
    
    return render(request, 'product/update_product.html', context)



# views.py

@login_required
def list_regular_products(request):
    # Get the search term from the URL query parameters, defaulting to an empty string if not present
    search_term = request.GET.get('search_term', '')

    # Filter products if there's a search term
    if search_term:
        queryset = Product.objects.filter(product_name__icontains=search_term)
    else:
        queryset = Product.objects.all()

    # Handle the "Sell" button click for regular users
    if request.method == 'POST' and 'sell_button' in request.POST:
        # Get the product ID from the POST request
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)

        # Only allow selling if the product has quantity available
        if product.total_quantity > 0:
            # Deduct 1 from the product's present_quantity and increment quantity_sold
            product.total_quantity -= 1
            product.quantity_sold += 1
            product.save()

        # After selling, redirect to the product list page
        return redirect('list_regular_products')  # Updated to the new view name

    # Prepare context for rendering
    context = {
        'product': queryset,
        'search_term': search_term,  # Pass the search term back to the template
    }

    return render(request, "product/home.html", context)


       


  

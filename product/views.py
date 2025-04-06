# Create your views here.
from django.shortcuts import get_object_or_404, render, redirect
from .models import Product
from django.http import HttpResponse
from .forms import ProductCreationForm, ProductupdateForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView, LogoutView
from stockmanage_lib import StockManager
import boto3
import logging

logger = logging.getLogger(__name__)

def listproducts(request):
    search_term = request.GET.get('search_term', '')
    queryset = StockManager.list_items(Product, search_term)
    context = {
        'product': queryset,
        'search_term': search_term,
    }
    return render(request, "product/home.html", context)

@login_required
@user_passes_test(lambda user: user.is_staff)
def addproducts(request):
    if request.method == 'POST':
        form = ProductCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listprod')
    else:
        form = ProductCreationForm()
    return render(request, 'product/addprod.html', {'form': form})

@login_required
@user_passes_test(lambda user: user.is_staff)
def delete_product(request, product_id):
    if request.method == 'POST':
        success = StockManager.delete_item(Product, product_id)
        return redirect('listprod')
    return redirect('listprod')

@login_required
@user_passes_test(lambda user: user.is_staff)
def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductupdateForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('listprod')
    else:
        form = ProductupdateForm(instance=product)
    context = {'form': form}
    return render(request, 'product/update_product.html', context)

@login_required
def list_regular_products(request):
    search_term = request.GET.get('search_term', '')
    queryset = StockManager.list_items(Product, search_term)
    if request.method == 'POST' and 'sell_button' in request.POST:
        product_id = request.POST.get('product_id')
        success = StockManager.sell_item(Product, product_id)
        return redirect('list_regular_products')
    context = {
        'product': queryset,
        'search_term': search_term,
    }
    return render(request, "product/home.html", context)

class CustomLoginView(LoginView):
    template_name = 'product/login.html'
    def form_valid(self, form):
        response = super().form_valid(form)
        try:
            sns = boto3.client('sns', region_name='eu-west-1')
            sns.publish(
                TopicArn='arn:aws:sns:eu-west-1:250738637992:login-notifications',
                Subject='User Login Notification',
                Message=f'User {self.request.user.username} has logged in.'
            )
        except Exception as e:
            logger.error(f'Failed to send login SNS notification: {e}')
        return response

class CustomLogoutView(LogoutView):
    template_name = 'product/logout.html'  # New logout template
    # Removed next_page since we’ll show a template instead
    def dispatch(self, request, *args, **kwargs):
        username = request.user.username if request.user.is_authenticated else 'Anonymous'
        try:
            sns = boto3.client('sns', region_name='eu-west-1')
            sns.publish(
                TopicArn='arn:aws:sns:eu-west-1:250738637992:login-notifications',
                Subject='User Logout Notification',
                Message=f'User {username} has logged out.'
            )
        except Exception as e:
            logger.error(f'Failed to send logout SNS notification: {e}')
        return super().dispatch(request, *args, **kwargs)
from django.urls import path
from . import views
from django.conf.urls.static import static  
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('listprod/',views.listproducts,name='listprod'),
    path('addprod/',views.addproducts,name='addproduct'),
    path('delete/<int:product_id>/', views.delete_product, name='delproduct'),
    path('update/<int:product_id>/', views.update_product, name='updproduct'),
    path('sell_product/', views.list_regular_products, name='list_regular_products'),  

    # Login and Logout
    path('login/', auth_views.LoginView.as_view(template_name='product/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='product/login'), name='logout'),  # Redirect to login after logout
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    

    

    
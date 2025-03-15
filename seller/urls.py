from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
# from .views import seller_dashboard, add_product, edit_seller_profile

app_name = "seller"  

urlpatterns = [
    path('shop/', views.shop, name="shop"),
    path('shop/add_prod/', views.add_prod, name="add_prod"),
    path('shop/add_cat/', views.add_cat, name="add_cat"),
    path('shop/edit_prod/<int:id>', views.edit_prod, name="edit_prod"),
    path('shop/edit_cat/<int:id>', views.edit_cat, name="edit_cat"),
    path('SellerRegistration/', views.SellerRegistration, name="SellerRegistration"),
    path('Sellerlogin/', views.Sellerlogin, name="Sellerlogin"),

    # path('dashboard/', seller_dashboard, name='seller_dashboard'),
    # path('add-product/', add_product, name='add_product'),
    # path('edit-profile/', edit_seller_profile, name='edit_seller_profile'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

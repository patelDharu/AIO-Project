from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
# from .views import seller_dashboard, add_product, edit_seller_profile

app_name = "seller"  

urlpatterns = [
    path('shop/', views.shop, name="shop"),
    path('orders/', views.orders_list, name='orders_list'),
    path('order/update/<int:orderid>/', views.order_update, name='order_update'),
    path('order/delete/<int:orderid>/', views.order_delete, name='order_delete'),
    path('users/', views.users_list, name='users_list'),
    path('user/update/<int:userid>/', views.user_update, name='user_update'),
    path('user/delete/<int:userid>/', views.user_delete, name='user_delete'),
    path('feedbacks/', views.feedbacks_list, name='feedbacks_list'),
    path('shop/add_prod/', views.add_prod, name="add_prod"),
    path('shop/add_cat/', views.add_cat, name="add_cat"),
    path('shop/edit_prod/<int:id>', views.edit_prod, name="edit_prod"),
    path('shop/edit_cat/<int:id>', views.edit_cat, name="edit_cat"),
    path('SellerRegistration/', views.SellerRegistration, name="SellerRegistration"),
    path('Sellerlogin/', views.Sellerlogin, name="Sellerlogin"),

    path('sub_category_one/', views.sub_category_one_list, name='sub_category_one_list'),
    path('sub_category_one/add/', views.sub_category_one_add, name='sub_category_one_add'),
    path('sub_category_one/update/<int:id>/', views.sub_category_one_update, name='sub_category_one_update'),
    path('sub_category_one/delete/<int:id>/', views.sub_category_one_delete, name='sub_category_one_delete'),

    path('sub_category/', views.sub_category_list, name='sub_category_list'),
    path('sub_category/add/', views.sub_category_add, name='sub_category_add'),
    path('sub_category/update/<int:id>/', views.sub_category_update, name='sub_category_update'),
    path('sub_category/delete/<int:id>/', views.sub_category_delete, name='sub_category_delete'),

    path('delete_cat/<int:id>/', views.delete_cat, name='delete_cat'),
    path('delete_prod/<int:id>/', views.delete_prod, name='delete_prod'),

    # path('dashboard/', seller_dashboard, name='seller_dashboard'),
    # path('add-product/', add_product, name='add_product'),
    # path('edit-profile/', edit_seller_profile, name='edit_seller_profile'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

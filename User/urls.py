from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path('logreg/', views.logreg, name="logreg"),
    path('login/', views.user_login, name='login'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('contact/', views.contact, name="contact"),
    path('about/', views.about, name="about"),
    path('shop/<int:category_id>/', views.shop, name='shop'),
    path('search/', views.search, name='search'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add-to-wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('add-to-cart-from-wishlist/<int:product_id>/<str:size>/', views.add_to_cart_from_wishlist, name='add_to_cart_from_wishlist'),
    path('men/<int:sub_category_id>/', views.men, name="men"),
    path('prod_details/<int:product_id>/', views.prod_details, name='prod_details'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('delete_cart/<int:cartid>/', views.delete_cart, name='delete_cart'),
    path('checkout/', views.checkout, name="checkout"),
    path('my_account/', views.my_account, name="my_account"),
    path('place-order/', views.place_order, name='place_order'),
    path('payment/', views.payment, name='payment'),
    path('payment/payment-handler/', views.paymenthandler, name='payment_handler'),
    path('orders/', views.orders, name="orders"),
    path('downloads/', views.downloads, name="downloads"),
    path('addresses/', views.addresses, name="addresses"),
    path('edit_account/', views.edit_account, name="edit_account"),
    path('track/', views.track, name="track"),
    path('wishlist/', views.wishlist, name="wishlist"),
    path('order/', views.order, name="order"),
    path('SellerRegistration/', views.SellerRegistration, name="SellerRegistration"),
    path('Sellerlogin/', views.Sellerlogin, name="Sellerlogin"),
    path('SellerProduct/', views.SellerProduct, name="SellerProduct"),
    path('SellerProfile/', views.SellerProfile, name="SellerProfile"),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

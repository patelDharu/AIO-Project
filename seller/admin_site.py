from django.contrib.admin import AdminSite
from .models import *
from django.contrib import admin

class SellerAdminSite(AdminSite):
    site_header = 'Seller Administration'
    site_title = 'Seller Admin Portal'
    index_title = 'Welcome to the Seller Admin Portal'

seller_admin_site = SellerAdminSite(name='seller_admin')

# Register your models
seller_admin_site.register(Seller, admin.ModelAdmin)
seller_admin_site.register(Category, admin.ModelAdmin)
seller_admin_site.register(Subcategory, admin.ModelAdmin)
seller_admin_site.register(GalleryItem, admin.ModelAdmin)
seller_admin_site.register(Product, admin.ModelAdmin)
seller_admin_site.register(Order, admin.ModelAdmin)
seller_admin_site.register(Offer, admin.ModelAdmin)
seller_admin_site.register(Payment, admin.ModelAdmin)
seller_admin_site.register(Feedback, admin.ModelAdmin)
seller_admin_site.register(Report, admin.ModelAdmin)
seller_admin_site.register(Notification, admin.ModelAdmin)
# seller_admin_site


from django.urls import path
from .permissions import SellerRequiredMixin

class SellerAdminSite(AdminSite):
    # (existing code)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', self.admin_view(SellerRequiredMixin.as_view(lambda request: self.index(request)), name='index'))
        ]
        return custom_urls + urls

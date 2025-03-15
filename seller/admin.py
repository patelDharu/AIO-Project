from django.contrib import admin
from .models import *


# admin.site.register(Seller)

# class Category_(admin.ModelAdmin):
#     list_display = ['name','image','description']
# admin.site.register(Category,Category_)

# class Subcategory_(admin.ModelAdmin):
#     list_display = ['category','name','description']
# admin.site.register(Subcategory,Subcategory_)

# class GalleryItem_(admin.ModelAdmin):
#     list_display = ['seller','title','description','image','price','created_at','updated_at']
    
# admin.site.register(GalleryItem,GalleryItem_) 

# class Product_(admin.ModelAdmin):
#     list_display = ['seller','name','price','category','description']
# admin.site.register(Product,Product_)

# class Order_(admin.ModelAdmin):
#     list_display = ['seller','product','quantity','order_date','status']
# admin.site.register(Order,Order_)

# class Offer_(admin.ModelAdmin):
#     list_display = ['seller','product','discount_percentage','start_date','end_date','description']
    
# admin.site.register(Offer,Offer_) 

# class Payment_(admin.ModelAdmin):
#     list_display = ['order','payment_date','amount','method','status']
    
# admin.site.register(Payment,Payment_) 

# class Feedback_(admin.ModelAdmin):
#     list_display = ['product','rating','comment','created_at']
    
# admin.site.register(Feedback,Feedback_) 

# class Report_(admin.ModelAdmin):
#     list_display = ['seller','report_date','content','report_type']
    
# admin.site.register(Report,Report_) 

# class Notification_(admin.ModelAdmin):
#     list_display = ['seller','message','created_at','is_read']
    
# admin.site.register(Notification,Notification_) 


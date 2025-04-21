from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
from .models import *
from io import BytesIO
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from seller.models import SellerPerson

# Register your models here.

class seller_(admin.ModelAdmin):
    list_display=['id','name','password','contact','email','address','join_date']


class payment_(admin.ModelAdmin):
    list_display = ['id','total_amount','payment_dattime','payment_type','transaction_id','status']

admin.site.register(feedback)
admin.site.register(Contact)

class offer_(admin.ModelAdmin):
    list_display = ['id','product_id','product_name','seller_name','title','start_date','end_date','is_active']

#admin.site.register(offer,offer_)

class generatereport_(admin.ModelAdmin):
    list_display = ['seller_id','seller_name','name','created_at','updated_at']

class cat_(admin.ModelAdmin):
    list_display = ['id','name']

#admin.site.register(category,cat_)

class sub_category_one_(admin.ModelAdmin):
    list_display = ['id','name']

#admin.site.register(sub_category_one,sub_category_one_)

class sub_cat_(admin.ModelAdmin):
    list_display = ['id','name','category','sub_category_one']

#admin.site.register(sub_category,sub_cat_)


class product_(admin.ModelAdmin):
    list_display = ['product_id','seller_id','name','description','price','sub_category','stock','offer','dotd']

admin.site.register(product,product_)


class UserProfile_(admin.ModelAdmin):
    list_display = ['userid','username','email','password','phone','address','zipcode','gender','registration_date']

#admin.site.register(UserProfile,UserProfile_)


class Cart_(admin.ModelAdmin):
    list_display = ['cartid','product','UserProfile','quantity','added_on']

class Size_(admin.ModelAdmin):
    list_display = ['N/A','S','M','L','XL','XXL','3XL','4XL','26','28','30']

admin.site.register(Size)    


#admin.site.register(Cart,Cart_)
#admin.site.register(Size)
#admin.site.register(Wishlist)

# class Order_(admin.ModelAdmin):
#     list_display = ['orderid','product','UserProfile','seller_id','ordered_at','quantity','total_price','payment_method','status']

#     def generate_report(self, request):
#         prod_sales = {}
#         total_quantity = 0
#         for order in Order.objects.exclude(payment_method='Razorpay'):
#             prod_name = order.product.name
#             if prod_name in prod_sales:
#                 prod_sales[prod_name] += 1
#             else:
#                 prod_sales[prod_name] = 1

#             total_quantity += 1

#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = 'inline; filename=Sales_Report.pdf'

#         buffer = BytesIO()
#         doc = SimpleDocTemplate(buffer, pagesize=letter, title='Sales Report')
#         elements = []

#         title_style = getSampleStyleSheet()['Title']
#         title = Paragraph("Sales Report", style=title_style)
#         elements.append(title)

#         order_data = [['Product Name', 'Total Sold Quantity']]  # Table headers

#         for prod_name, total_sold in prod_sales.items():
#             order_data.append([prod_name, str(total_sold)])

#         order_data.append(['Total', str(total_quantity)])

#         order_table = Table(order_data)

#         order_table.setStyle(TableStyle([
#             ('GRID', (0, 0), (-1, -1), 0.5, (0, 0, 0)),
#             ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
#             ('BACKGROUND', (0, 0), (-1, 0), (0.5, 0.5, 0.5)),
#             ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1)),
#             ('FONTSIZE', (0, 0), (-1, -1), 10),
#             ('BACKGROUND', (-1, -1), (-1, -1), (0.7, 0.7, 0.7)),
#         ]))

#         elements.append(order_table)

#         doc.build(elements)

#         pdf_content = buffer.getvalue()
#         buffer.close()
#         response.write(pdf_content)

#         return response

#     def get_urls(self):
#         urls = super().get_urls()
#         custom_url = [path('order_report/', self.generate_report), ]
#         return custom_url + urls


# admin.site.register(Order,Order_)

# class seller_(admin.ModelAdmin):
#     list_display = ['username','email']

# admin.site.register(SellerPerson,seller_)
class Order_(admin.ModelAdmin):
    list_display = ['orderid','product','UserProfile','seller_id','ordered_at','quantity','total_price','payment_method','status']

    def generate_report(self, request):
        start_date = request.GET["start"]
        end_date = request.GET["end"]
        prod_name = request.GET.get("prod_name")
        seller_id = request.GET.get("seller_id")
        total_quantity = 0
        total_sales = 0

        if seller_id:
            if prod_name:
                orders = Order.objects.exclude(payment_method__isnull=True).filter(ordered_at__date__range=[start_date, end_date], product__name__icontains=prod_name, product__seller_id=int(seller_id))
            else:
                orders = Order.objects.exclude(payment_method__isnull=True).filter(ordered_at__date__range=[start_date, end_date], product__seller_id=int(seller_id))
        else:
            if prod_name:
                orders = Order.objects.exclude(payment_method__isnull=True).filter(ordered_at__date__range=[start_date, end_date], product__name__icontains=prod_name)
            else:
                orders = Order.objects.exclude(payment_method__isnull=True).filter(ordered_at__date__range=[start_date, end_date])

        if not orders:
            if seller_id:
                return HttpResponse(
                    "<script>alert('No records found!!');window.location.href='/seller/orders/';</script>")
            else:
                return HttpResponse(
                    "<script>alert('No records found between selected range!!');window.location.href='/admin/User/order/';</script>")

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename=Sales_Report.pdf'

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, title='Sales Report')
        elements = []

        title_style = getSampleStyleSheet()['Title']
        title = Paragraph("Sales Report", style=title_style)
        elements.append(title)

        order_data = [['User Name', 'Product Name','Total Amount', 'Booked Date']]
        for order in orders:
            order_data.append([order.UserProfile.username, order.product.name, f'Rs.{int(order.total_price)}', order.ordered_at.date()])
            total_quantity += 1
            total_sales += int(order.total_price)

        order_data.append(['', '', 'Total Sales:', f'Rs.{total_sales}'])
        order_data.append(['', '', 'Total Orders:', str(total_quantity)])

        order_table = Table(order_data)

        order_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, (0, 0, 0)),
            ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
            ('BACKGROUND', (0, 0), (-1, 0), (0.5, 0.5, 0.5)),
            ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1)),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BACKGROUND', (-1, -1), (-1, -1), (0.7, 0.7, 0.7)),
        ]))

        elements.append(order_table)

        doc.build(elements)

        pdf_content = buffer.getvalue()
        buffer.close()
        response.write(pdf_content)

        return response

    def get_urls(self):
        urls = super().get_urls()
        custom_url = [path('order_report/', self.generate_report), ]
        return custom_url + urls


admin.site.register(Order,Order_)

class seller_(admin.ModelAdmin):
    list_display = ['username','email']

    def generate_report(self, request):
        total_quantity = 0

        orders = SellerPerson.objects.all()

        if not orders:
            return HttpResponse(
                "<script>alert('No records found!!');window.location.href='/admin/seller/sellerperson/';</script>")

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename=Sellers_Report.pdf'

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, title='Sellers Report')
        elements = []

        title_style = getSampleStyleSheet()['Title']
        title = Paragraph("Sellers Report", style=title_style)
        elements.append(title)

        order_data = [['Vendor Name', 'Joined Date']]
        for order in orders:
            order_data.append([order.username, order.join_date])
            total_quantity += 1

        order_data.append(['Total Sellers:', str(total_quantity)])

        order_table = Table(order_data)

        order_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, (0, 0, 0)),
            ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
            ('BACKGROUND', (0, 0), (-1, 0), (0.5, 0.5, 0.5)),
            ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1)),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BACKGROUND', (-1, -1), (-1, -1), (0.7, 0.7, 0.7)),
        ]))

        elements.append(order_table)

        doc.build(elements)

        pdf_content = buffer.getvalue()
        buffer.close()
        response.write(pdf_content)

        return response

    def get_urls(self):
        urls = super().get_urls()
        custom_url = [path('order_report/', self.generate_report), ]
        return custom_url + urls

admin.site.register(SellerPerson,seller_)
admin.site.register(Progress)
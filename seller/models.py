from django.db import models
from django.contrib.auth.models import User

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=100)
    description = models.TextField()

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class Subcategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.category.name} - {self.name}"    
    
class GalleryItem(models.Model):
    seller = models.ForeignKey(Seller, related_name='gallery_items', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='gallery_images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title    

class Product(models.Model):
    seller = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    
class Order(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ])

    def __str__(self):
        return    
     
class Offer(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return 
    
class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=50, choices=[
        ('UPI', 'UPI'),
        ('Cash on Delivery', 'Cash on Delivery'),
    ])
    status = models.CharField(max_length=50, choices=[
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ])

    def __str__(self):
        return f"Payment for Order #{self.order.id} - {self.amount}"    


class Feedback(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()  
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 
    
class Report(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    report_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    report_type = models.CharField(max_length=50, choices=[
        ('Sales', 'Sales'),
        ('Inventory', 'Inventory'),
        ('Performance', 'Performance'),
    ])
    related_product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    related_order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.report_type} Report - {self.seller.name}"

class Notification(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.seller.name} - {self.message[:20]}..."        


class SellerPerson(models.Model): 
    username = models.CharField(max_length=100,unique=True)
    email = models.EmailField()
    password1 = models.CharField(max_length=255,)
    password2 = models.CharField(max_length=255)
    contact = models.CharField(max_length=10, default="")
    address = models.TextField(default="")
    join_date = models.DateField(auto_now_add=True, blank=True, null=True)
    
    REQUIRED_FIELDS = ['username','email','password1','password2','contact','address']
    def __str__(self):
        return self.username

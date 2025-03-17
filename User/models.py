from django.utils import timezone
from django.db import models

# Create your models here.

class UserProfile(models.Model):
    CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    userid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=6, blank=True, null=True)
    gender = models.CharField(max_length=50, choices=CHOICES)
    registration_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username


class seller(models.Model):
      name=models.CharField(max_length=50)
      password=models.CharField(max_length=8)
      contact=models.CharField(max_length=10)
      email=models.EmailField()
      address=models.TextField()
      join_date = models.DateField(auto_now_add=True)
      
      def _str_(self):
        return self.name
      
class payment(models.Model):
      total_amount = models.PositiveIntegerField()
      payment_dattime = models.DateTimeField(auto_now=True)
      payment_type = models.CharField(max_length=20)
      transaction_id = models.CharField(max_length=100)
      status = models.CharField(max_length=20, default='PENDING')

      def _str_(self):
        return self.name  
      
class feedback(models.Model):
      customer_id = models.PositiveIntegerField()
      product_name = models.CharField(max_length=50)  
      content = models.TextField(help_text="Feedback content")
      rating = models.PositiveIntegerField(help_text="Rating out of 5")
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)

      def _str_(self):
        return self.name

class offer(models.Model):
     product_id = models.PositiveIntegerField()
     product_name = models.CharField(max_length=50)
     seller_name = models.CharField(max_length=50)
     title = models.CharField(max_length=100)
     start_date = models.DateField()
     end_date = models.DateField()
     is_active = models.BooleanField(default=True)

     def _str_(self):
        return self.name

class generatereport(models.Model):
    seller_id = models.PositiveIntegerField()
    seller_name = models.CharField(max_length=50)
    name = models.CharField(max_length=100, help_text="Name of the report")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
     

    def _str_(self):
        return self.name

class category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='category',blank=True)

class sub_category_one(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class sub_category(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(category,blank=True,on_delete=models.CASCADE)
    sub_category_one = models.ForeignKey(sub_category_one,blank=True,on_delete=models.CASCADE)
    #image = models.ImageField( upload_to='subcategory', height_field=None, width_field=None)

    def __str__(self):
        return str(self.name)

class Size(models.Model):
    SIZES = (
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
        ('3XL', '3XL'),
        ('4XL', '4XL'),
    )
    size = models.CharField(choices=SIZES, max_length=50)

    def __str__(self):
        return self.size


class product(models.Model):
    product_id = models.AutoField(primary_key=True)
    seller_id = models.PositiveIntegerField()
    name = models.CharField(max_length=150)
    description = models.TextField()
    dotd = models.BooleanField(default=False, verbose_name="Deal of the day? (Make sure to change price)")
    price = models.PositiveIntegerField()
    sizes = models.ManyToManyField(Size)
    #category = models.ForeignKey(category,on_delete=models.CASCADE,blank=True)
    sub_category = models.ForeignKey(sub_category, on_delete=models.CASCADE,blank=True)
    stock = models.PositiveIntegerField()
    offer = models.BooleanField(default=False)
    gallery = models.ImageField(upload_to='gallery/', blank=True, null=True)
    img2 = models.ImageField(upload_to='gallery/', blank=True, null=True)
    img3 = models.ImageField(upload_to='gallery/', blank=True, null=True)
    img4 = models.ImageField(upload_to='gallery/', blank=True, null=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    cartid = models.AutoField(primary_key=True)
    product = models.ForeignKey(product, to_field='product_id', on_delete=models.CASCADE)
    UserProfile = models.ForeignKey(UserProfile, to_field='userid', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=50, blank=True, null=True)
    added_on = models.DateTimeField(auto_now_add=True)

    def get_total_price(self):
        return self.product.price * self.quantity


class Wishlist(models.Model):
    wishlist_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, to_field='userid', on_delete=models.CASCADE)
    size = models.CharField(max_length=50, blank=True, null=True)  # Add size field here
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wishlist item for {self.user_profile} - {self.product.name} ({self.size})"

    


class Order(models.Model):
    CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('RAZORPAY', 'RAZORPAY'),
    ]
    orderid = models.AutoField(primary_key=True)
    product = models.ForeignKey(product, to_field='product_id', on_delete=models.CASCADE)
    UserProfile = models.ForeignKey(UserProfile, to_field='userid', on_delete=models.CASCADE)
    seller_id = models.PositiveIntegerField()
    ordered_at = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=50, blank=True, null=True)
    total_price = models.DecimalField(max_digits=50, decimal_places=2)
    admin_cut = models.DecimalField(max_digits=50, decimal_places=2, verbose_name="Admin Cut (10%)", default=0)
    fname = models.CharField(max_length=150)
    lname = models.CharField(max_length=150)
    company_name = models.CharField(max_length=150, blank=True, null=True)
    country = models.CharField(max_length=150)
    street_address= models.CharField(max_length=150)
    postcode = models.CharField(max_length=150, blank=True, null=True)
    city = models.CharField(max_length=150)
    phone = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    order_note = models.CharField(max_length=150, blank=True, null=True)
    payment_method = models.CharField(max_length=20,choices=CHOICES, blank=True, null=True)

    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return self.status
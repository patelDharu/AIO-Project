from django.conf import settings
from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import render,redirect,HttpResponse, get_object_or_404 
from django.http import HttpResponseRedirect
import razorpay
from seller.models import SellerPerson
from django.contrib import messages 
from django.contrib.auth.hashers import make_password,check_password

from .admin import product_
from .models import *
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


# razorpay client config
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

# # Create your views here.


def index(request):
    catdata = category.objects.all()
    sub_category_onedata = sub_category_one.objects.all()
    sub_categorydata = sub_category.objects.all()
    dotd = product.objects.filter(dotd=True)
    new_arrival = get_object_or_404(category, id=1)
    new_arrival_prods = product.objects.filter(sub_category__category=new_arrival).order_by('-product_id')
    offers = product.objects.filter(offer=True).order_by('-product_id')
    return render(request, "index.html",{'main_category':catdata,'sub_category_one':sub_category_onedata,'sub_category':sub_categorydata,'dotd':dotd, 'new_arrival_prods':new_arrival_prods, 'offers': offers})



def logreg(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('c_password')
        phone = request.POST.get('phone')
        address=request.POST.get('address')
        zipcode=request.POST.get('zipcode')
        gender=request.POST.get('gender')


        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        elif UserProfile.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken. Please choose a different one.')
        elif UserProfile.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered. Please use a different email.')
        else:
            user = UserProfile(username=username, email=email, password=make_password(password), phone=phone,address=address,zipcode=zipcode,gender=gender)
            user.save()
            messages.success(request, 'Registration successful!')
            return redirect('index')

    catdata = category.objects.all()
    sub_category_onedata = sub_category_one.objects.all()
    sub_categorydata = sub_category.objects.all()
    param = {
        'main_category':catdata,
        'sub_category_one':sub_category_onedata,
        'sub_category':sub_categorydata
    }
    return render(request, "Accounts/logreg.html", param)


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email','username')
        password = request.POST.get('password')
        try:
            user = UserProfile.objects.get(email=email)
            if check_password(password, user.password):
                request.session['email'] = user.email
                messages.success(request, 'Login successful!')
                return redirect('index')
            else:
                messages.error(request, 'Invalid password.')
        except UserProfile.DoesNotExist:
            messages.error(request, 'User does not exist.')
            return redirect("logreg")
    return render(request, 'index.html')

def user_logout(request):
    if 'email' in request.session:
        del request.session['email']
    logout(request)
    messages.success(request,'Logged out successfully!')
    return redirect('index')

def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        c = Contact.objects.create(name=name, email=email, message=message)
        c.save()
        return HttpResponse("<script>alert('Message sent!!!');window.location.href='/contact/';</script>")
    catdata = category.objects.all()
    sub_category_onedata = sub_category_one.objects.all()
    sub_categorydata = sub_category.objects.all()
    param = {
        'main_category': catdata,
        'sub_category_one': sub_category_onedata,
        'sub_category': sub_categorydata,
    }
    return render(request, "contact.html", param)


def about(request):
    catdata = category.objects.all()
    sub_category_onedata = sub_category_one.objects.all()
    sub_categorydata = sub_category.objects.all()
    param = {
        'main_category': catdata,
        'sub_category_one': sub_category_onedata,
        'sub_category': sub_categorydata,
    }
    return render(request, "about.html", param)


def shop(request, category_id):
    categorys = get_object_or_404(category, id=category_id)
    products = product.objects.filter(sub_category__category=categorys)
    catdata = category.objects.all()
    sub_category_onedata = sub_category_one.objects.all()
    sub_categorydata = sub_category.objects.all()
    context = {
        'category': categorys,
        'products': products,
        'main_category': catdata,
        'sub_category_one': sub_category_onedata,
        'sub_category': sub_categorydata,
    }
    
    return render(request, 'shop.html', context)

def men(request,sub_category_id):
    sub_categorys = get_object_or_404(sub_category, id=sub_category_id)
    products = product.objects.filter(sub_category=sub_categorys)
    catdata = category.objects.all()
    sub_category_onedata = sub_category_one.objects.all()
    sub_categorydata = sub_category.objects.all()
    param = {
        'main_category': catdata,
        'sub_category_one': sub_category_onedata,
        'sub_category': sub_categorydata,
        'products': products,
        'subcategory': sub_categorys,
    }

    return render(request, 'men.html', param)



def search(request):
    query = request.GET.get("query")
    sub_categorys = f"Results for {str(query)}"
    products = product.objects.filter(name__icontains=str(query))

    catdata = category.objects.all()
    sub_category_onedata = sub_category_one.objects.all()
    sub_categorydata = sub_category.objects.all()
    param = {
        'main_category': catdata,
        'sub_category_one': sub_category_onedata,
        'sub_category': sub_categorydata,
        'products': products,
        'subcategory': sub_categorys,
    }

    return render(request, 'men.html', param)

def prod_details(request, product_id):
    products = get_object_or_404(product, product_id=product_id)  # Fetch the product by ID
    reviews = feedback.objects.filter(product__product_id=product_id).order_by('-id')
    catdata = category.objects.all()
    sub_category_onedata = sub_category_one.objects.all()
    sub_categorydata = sub_category.objects.all()
    param = {
        'main_category': catdata,
        'sub_category_one': sub_category_onedata,
        'sub_category': sub_categorydata,
        'products': products,
        'reviews': reviews,
    }
    return render(request, 'prod_details.html', param)



def cart(request):
    email = request.session.get('email')
    total_price=0
    if email:
        # Get the UserProfile associated with the email
        #user_profile = UserProfile.objects.get(email=email)

        # Filter Cart items based on the UserProfile
        cart_items = Cart.objects.filter(UserProfile__email=email)
        total_price = sum(item.get_total_price() for item in cart_items)
    else:
        cart_items = []

    catdata = category.objects.all()
    sub_category_onedata = sub_category_one.objects.all()
    sub_categorydata = sub_category.objects.all()
    param = {
        'main_category': catdata,
        'sub_category_one': sub_category_onedata,
        'sub_category': sub_categorydata,
        'cart_items': cart_items,
        'total_price': total_price
    }

    return render(request, 'cart.html', param)

def add_to_cart(request, product_id):
    products = get_object_or_404(product, product_id=product_id)
    email = request.session.get('email')
    size = request.POST.get("my_size")
    quantity = int(request.POST.get("quantity", 1))
    update = request.POST.get("update")

    if update == "True":
        cart_id = int(request.POST.get("cart_id"))
        cart_item = Cart.objects.get(cartid=cart_id)
        cart_item.size = size
        cart_item.quantity = quantity
        cart_item.save()
        return redirect("/cart/")

    if quantity <= 0:
        messages.warning(request, 'Invalid Quantity!')
        return redirect('prod_details', product_id)

    if email:
        # Get or create the UserProfile based on the email
        user_profile = get_object_or_404(UserProfile, email=email)

        # Get or create the cart item associated with the user and product
        cart_item, created = Cart.objects.get_or_create(
        product=products,
        UserProfile=user_profile,
        size=size,
        defaults={'quantity': quantity}
    )

        if not created:
            # If the cart item already exists, just update the quantity
            cart_item.quantity += quantity
            cart_item.save()
           
    else:
        return redirect('logreg')
    messages.success(request, 'Item Added!')
    return redirect('cart')

def delete_cart(request, cartid):
    cart = get_object_or_404(Cart, cartid=cartid)
    cart.delete()
    messages.success(request, 'Item Removed successfully!')
    return redirect('cart')


def checkout(request):
    email = request.session.get('email')
    total_price=0
    if email:
        # Get the UserProfile associated with the email
        #user_profile = UserProfile.objects.get(email=email)

        # Filter Cart items based on the UserProfile
        cart_items = Cart.objects.filter(UserProfile__email=email)
        total_price = sum(item.get_total_price() for item in cart_items)
    else:
        cart_items = []

    catdata = category.objects.all()
    sub_category_onedata = sub_category_one.objects.all()
    sub_categorydata = sub_category.objects.all()
    param = {
        'main_category': catdata,
        'sub_category_one': sub_category_onedata,
        'sub_category': sub_categorydata,
        'cart_items': cart_items,
        'total_price': total_price
    }

    return render(request, 'checkout.html', param)


def my_account(request):
    catdata = category.objects.all()
    sub_category_onedata = sub_category_one.objects.all()
    sub_categorydata = sub_category.objects.all()
    param = {
        'main_category': catdata,
        'sub_category_one': sub_category_onedata,
        'sub_category': sub_categorydata,
    }
    return render(request, "Accounts/my_account.html", param)


def place_order(request):
    if request.method == 'POST':
        # Get the user's billing info from the form
        fname = request.POST.get('billing_first_name')
        lname = request.POST.get('billing_last_name')
        company_name = request.POST.get('billing_company_name')
        country = request.POST.get('billing_country')
        street_address = request.POST.get('billing_address_1')
        postcode = request.POST.get('billing_postcode')
        city = request.POST.get('billing_city')
        phone = request.POST.get('billing_phone')
        email = request.POST.get('billing_email')
        order_note = request.POST.get('order_note')
        payment_method = request.POST.get('payment_method')

        
        email = request.session.get('email')
        if email:
            user_profile = get_object_or_404(UserProfile, email=email)
            cart_items = Cart.objects.filter(UserProfile__email=email)

            if cart_items.exists()  and payment_method == 'COD':
                for item in cart_items:
                    total_price = item.get_total_price()
                    s = Order.objects.create(
                        product=item.product,
                        UserProfile=user_profile,
                        seller_id=item.product.seller_id,
                        ordered_at=timezone.now(),
                        quantity=item.quantity,
                        size=item.size,
                        admin_cut=(total_price * 0.10),
                        total_price=total_price,
                        status='Pending',
                        fname=fname,
                        lname=lname,
                        company_name=company_name,
                        country=country,
                        street_address=street_address,
                        postcode=postcode,
                        city=city,
                        phone=phone,
                        email=email,
                        order_note=order_note,
                        payment_method=payment_method
                    )
                    s.save()
                    s.order_payment_id = s.orderid
                    s.save()

                cart_items.delete()                
                messages.success(request, 'Your order has been placed successfully!')
                return redirect('orders')  

            elif cart_items.exists() and payment_method == 'RAZORPAY':
                total_price1 = sum(item.get_total_price() for item in cart_items)
                amount = int(total_price1 * 100)
                
                for item in cart_items:
                    total_price = item.get_total_price()
                    s = Order.objects.create(
                        product=item.product,
                        UserProfile=user_profile,
                        seller_id=item.product.seller_id,
                        ordered_at=timezone.now(),
                        quantity=item.quantity,
                        size=item.size,
                        admin_cut=(total_price * 0.10),
                        total_price=total_price,
                        status='Pending',
                        fname=fname,
                        lname=lname,
                        company_name=company_name,
                        country=country,
                        street_address=street_address,
                        postcode=postcode,
                        city=city,
                        phone=phone,
                        email=email,
                        order_note=order_note,
                        payment_method=payment_method
                    )
                    s.save()
                    s.order_payment_id = "TBU"
                    s.save()

                request.session['amount'] = amount
                return redirect('payment')  # Ensure this matches the Razorpay payment page URL

            else:
                messages.error(request, 'No items in cart. Please add items to your cart before placing an order.')
                return redirect('cart')
        else:
            messages.error(request, 'Please log in to place an order.')
            return redirect('logreg')


def payment(request):
    amount = request.session.get('amount')
    currency = request.session.get('currency', 'INR')
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(
        dict(
            amount=amount,
            currency='INR',
            payment_capture='0'
        )
    )

    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    my_orders = Order.objects.filter(order_payment_id="TBU")
    for mo in my_orders:
        mo.order_payment_id = razorpay_order_id
        mo.save()

    callback_url = str(request.is_secure() and "https" or "http" + "://" + request.get_host() + "/payment/payment-handler/")
    context = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount,
        'currency': currency,
        'callback_url': callback_url,
        'total_amount': amount / 100,
    }
    return render(request, 'payment.html', context)


# ----------------------- VERIFY SIGNATURE  -----------------------------------
@csrf_exempt
def paymenthandler(request):
    # only accept POST request.
    if request.method == "POST":
        amount = request.session.get('amount')
        try:
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')

            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # verify the payment signature.

            signature = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if signature is not None:

                try:
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)


                     # Fetch the user profile to delete cart items
                    email = request.session.get('email')
                    if email:
                        user_profile = get_object_or_404(UserProfile, email=email)
                        cart_items = Cart.objects.filter(UserProfile=user_profile)

                        # Delete cart items after successful payment
                        cart_items.delete()
                    # render success page on successful caputre of payment
                    return render(request, 'payment-successful.html')
                except Exception as e:
                    print(e)
                    # if there is an error while capturing payment.
                    return render(request, 'payment-aborted.html')
            else:
                print('signature verification fails')
                # if signature verification fails.
                return render(request, 'payment-fail.html')
        except Exception as e:
            print(e)
            return render(request, 'payment-aborted.html')
    else:
        # if other than POST request is made.
        return render(request, 'payment-aborted.html')


def orders(request):
    email = request.session.get('email')
    if email:
        user_profile = get_object_or_404(UserProfile, email=email)
        orders = Order.objects.filter(UserProfile=user_profile).order_by('-ordered_at')
        catdata = category.objects.all()
        sub_category_onedata = sub_category_one.objects.all()
        sub_categorydata = sub_category.objects.all()
        param = {
            'main_category': catdata,
            'sub_category_one': sub_category_onedata,
            'sub_category': sub_categorydata,
            'orders': orders
        }
        return render(request, 'Accounts/orders.html', param)
    else:
        messages.error(request, 'Please log in to view your orders.')
        return redirect('logreg')


def downloads(request):
    return render(request, "Accounts/downloads.html")


def addresses(request):
    return render(request, "Accounts/addresses.html")


def edit_account(request):
    return render(request, "Accounts/edit_account.html")


def track(request):
    return render(request, "track.html")


def wishlist(request):
    email = request.session.get('email')
    if email:
        # Get the user profile based on the session email
        user_profile = get_object_or_404(UserProfile, email=email)

        # Get all the products in the user's wishlist, including the size field
        wishlist_items = Wishlist.objects.filter(user_profile=user_profile)

        catdata = category.objects.all()
        sub_category_onedata = sub_category_one.objects.all()
        sub_categorydata = sub_category.objects.all()
        param = {
            'main_category': catdata,
            'sub_category_one': sub_category_onedata,
            'sub_category': sub_categorydata,
            'orders': orders,
            "wishlist_items": wishlist_items
        }

        return render(request, "wishlist.html", param)
    else:
        return redirect('logreg')


def add_to_wishlist(request, product_id):
    email = request.session.get('email')

    if email:
        prod = get_object_or_404(product, product_id=product_id)
        size = request.POST.get('my_size')
        quantity = int(request.POST.get('quantity', 1))

        # Get or create the UserProfile based on the email
        user_profile = get_object_or_404(UserProfile, email=email)

        # Create or update the wishlist item
        wishlist_item, created = Wishlist.objects.get_or_create(
            product=prod,
            user_profile=user_profile,
            size=size,
            defaults={'quantity': quantity}
        )

        if created:
            # Successfully added to wishlist
            messages.success(request, 'Item added to your Wishlist!')
        else:
            wishlist_item.quantity += quantity
            wishlist_item.save()
            messages.info(request, 'Item already exists in your Wishlist, so updated!')

        return redirect('wishlist')  # Redirect to the wishlist page
    else:
        return redirect('logreg')

def add_to_cart_from_wishlist(request, product_id, size, q):
    email = request.session.get('email')
    quantity = int(q)
    if email:
        # Get the user profile based on the email in the session
        user_profile = get_object_or_404(UserProfile, email=email)
        prod = get_object_or_404(product, product_id=product_id)

        # Get or create the cart item for the user and product
        cart_item, created = Cart.objects.get_or_create(
            product=prod,
            UserProfile=user_profile,
            size=size,
            defaults={'quantity': quantity}
        )
        if not created:
            # If the item already exists in the cart, just increase the quantity
            cart_item.quantity += quantity
            cart_item.save()

        # Remove the product from the wishlist after it's added to the cart
        Wishlist.objects.filter(user_profile=user_profile, product=prod).delete()

        messages.success(request, f"'{prod.name}' has been added to your cart!")
        return redirect('wishlist')  # Redirect back to the wishlist page
    else:
        return redirect('logreg')



def order(request):
    return render(request,"seller/order.html")



    
def SellerRegistration(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        Email1 = request.POST.get('email')
        pass1 = request.POST.get('p1')
        pass2 = request.POST.get('p2')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        if SellerPerson.objects.filter(username=uname).exists():
            messages.info(request, 'Username already exists. Try another username.')
        elif SellerPerson.objects.filter(email=Email1).exists():
            messages.info(request, 'Email Id already exists. Try another email.')
        else:
            if pass1 == pass2:  
                myuser = SellerPerson(username=uname, email=Email1, password1=pass1, password2=pass2, contact=phone, address=address)
                myuser.save()
                messages.success(request, 'Registration successful!')
                return redirect('Sellerlogin')  
            else:
                messages.error(request, 'Passwords do not match!')
    return render(request,"seller/SellerRegistration.html")


def Sellerlogin(request):
     if request.method == 'POST':
        try:
            user=SellerPerson.objects.get(email=request.POST['email'])
            if user.password1 == request.POST['p1']:
                request.session['ven_email'] = user.email

                return redirect('seller:shop')  
            else:
                p='Password Dose Not Match'
                return render(request,'seller/Sellerlogin.html',{'p':p})
        except Exception as e:
             print(e,"errrooorrr")
             m='Email Id And Password Dose Not Exixt!'
             return render(request,'seller/Sellerlogin.html',{'m':m})
     else:
        return render(request,"seller/Sellerlogin.html")

def SellerProfile(request):
    return render(request,"seller/SellerProfile.html")

def SellerProduct(request):
    return render(request,"seller/SellerProduct.html")

def FeedBack(request):
    if request.method == "POST":
        current_email = request.session['email']
        name = UserProfile.objects.get(email=current_email)
        email = name.email
        rating = request.POST['rating']
        content = request.POST['comment']
        product_id = int(request.POST['prod_id'])
        prod = product.objects.get(product_id=product_id)

        f = feedback.objects.create(name=name, email=email, product=prod, content=content, rating=rating)
        f.save()

        return redirect(f"/prod_details/{product_id}/")

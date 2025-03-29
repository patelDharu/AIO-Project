from django.shortcuts import render, redirect, get_object_or_404
from User.models import *
from django.contrib import messages
from .forms import *

# Create your views here.

def SellerRegistration(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        Email1 = request.POST.get('email')
        pass1 = request.POST.get('p1')
        pass2 = request.POST.get('p2')

        if SellerPerson.objects.filter(email=Email1).exists():
            messages.info(request, 'Email Id already exists. Try another email.')
        else:
            if pass1 == pass2:  
                myuser = SellerPerson(username=uname, email=Email1, password1=pass1, password2=pass2)
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



def shop(request):
    if 'ven_email' in request.session:
        s = SellerPerson.objects.get(email=request.session['ven_email'])
        s_id = s.id
        cat = category.objects.all()
        pro = product.objects.filter(seller_id=s_id).order_by('-product_id')
        request.session['seller_id'] = s_id
        return render(request,"seller/shop.html",{'cat':cat,'pro':pro})
    else:
        return redirect("seller:Sellerlogin")


def add_cat(request):
    if request.method == "POST":
        name = request.POST.get('cname')
        image = request.FILES.get('image')
        image2 = request.FILES.get('image2')
        redirect_url1 = request.POST.get('redirect_url1')
        redirect_url2 = request.POST.get('redirect_url2')
        visibility = 'visibility' in request.POST

        new_category = category(
            name=name,
            image=image,
            image2=image2,
            redirect_url1=redirect_url1,
            redirect_url2=redirect_url2,
            visibility=visibility
        )
        new_category.save()

        return redirect('seller:shop')
    return render(request, "seller/add_cat.html")

# Edit category
def edit_cat(request, id):
    cat = category.objects.get(id=id)
    if request.method == 'POST':
        cat.name = request.POST['cname']
        if 'image' in request.FILES:
            cat.image = request.FILES['image']
        if 'image2' in request.FILES:
            cat.image2 = request.FILES['image2']
        cat.redirect_url1 = request.POST['redirect_url1']
        cat.redirect_url2 = request.POST['redirect_url2']
        cat.visibility = 'visibility' in request.POST
        cat.save()

        return render(request, "seller/add_cat.html", {'cat': cat})
    else:
        return render(request, "seller/add_cat.html", {'cat': cat})

def add_prod(request):
    sub_cat = sub_category.objects.all()
    sizes = Size.objects.all()
    s_id = request.session['seller_id'] # Seller ID
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('comment')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        offer = 'offer' in request.POST  # If the offer checkbox is checked
        dotd = 'dotd' in request.POST  # If the deal-of-the-day checkbox is checked
        sub_category_id = request.POST.get('category')  # Get the selected subcategory

        # Handle the image uploads
        gallery_image = request.FILES.get('gallery')  # main image
        img2 = request.FILES.get('img2')
        img3 = request.FILES.get('img3')
        img4 = request.FILES.get('img4')

        # Get the selected subcategory
        subcategory = sub_category.objects.get(id=sub_category_id)

        # Create the product instance
        new_product = product(
            seller_id=s_id,  # Store seller ID in session
            name=name,
            description=description,
            price=price,
            stock=stock,
            offer=offer,
            dotd=dotd,
            sub_category=subcategory
        )

        # Save the product without images first
        new_product.save()

        # Handle saving the sizes (multiple sizes selected)
        selected_sizes = request.POST.getlist('sizes')  # Get the selected size IDs
        for size_id in selected_sizes:
            selected_size = Size.objects.get(id=size_id)
            new_product.sizes.add(selected_size)  # Add the sizes to the product

        # Handle saving the images
        if gallery_image:
            new_product.gallery = gallery_image
        if img2:
            new_product.img2 = img2
        if img3:
            new_product.img3 = img3
        if img4:
            new_product.img4 = img4

        # Save the product again after adding images and sizes
        new_product.save()

        # Redirect to product list page (you can change the URL here)
        return redirect('seller:shop')
    return render(request,"seller/add_prod.html",{'sub_cat':sub_cat, 'sizes': sizes})

def edit_prod(request, id):
    pro = product.objects.get(product_id=id)
    sub_cat = sub_category.objects.all()
    sizes = Size.objects.all()  # Get all sizes for the dropdown

    if request.method == "POST":
        # Get form data
        name = request.POST.get('name')
        description = request.POST.get('comment')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        offer = 'offer' in request.POST  # If the offer checkbox is checked
        dotd = 'dotd' in request.POST  # If the deal-of-the-day checkbox is checked
        sub_category_id = request.POST.get('category')  # Get the selected subcategory

        # Handle the image uploads
        gallery_image = request.FILES.get('gallery')  # main image
        img2 = request.FILES.get('img2')
        img3 = request.FILES.get('img3')
        img4 = request.FILES.get('img4')

        # Handle the selected subcategory
        subcategory = sub_category.objects.get(id=sub_category_id)

        # Update the product instance
        pro.name = name
        pro.description = description
        pro.price = price
        pro.stock = stock
        pro.offer = offer
        pro.dotd = dotd
        pro.sub_category = subcategory

        # Handle updating sizes (multiple sizes selected)
        selected_sizes = request.POST.getlist('sizes')  # Get the selected size IDs
        pro.sizes.clear()  # Clear previous sizes (if any)
        for size_id in selected_sizes:
            selected_size = Size.objects.get(id=size_id)
            pro.sizes.add(selected_size)  # Add the new sizes

        # Handle updating images (if provided)
        if gallery_image:
            pro.gallery = gallery_image
        if img2:
            pro.img2 = img2
        if img3:
            pro.img3 = img3
        if img4:
            pro.img4 = img4

        # Save the updated product
        pro.save()

        # Redirect to product list or another page after editing
        return redirect('seller:shop')

    # Render the edit product page
    return render(request, "seller/add_prod.html", {'pro': pro, 'sub_cat': sub_cat, 'sizes': sizes})


def orders_list(request):
    s = SellerPerson.objects.get(email=request.session['ven_email'])
    s_id = s.id
    orders = Order.objects.filter(seller_id=s_id).order_by('-orderid')
    return render(request, 'seller/orders_list.html', {'orders': orders, 'seller_id': s_id})


# View to update an order
def order_update(request, orderid):
    order = get_object_or_404(Order, orderid=orderid)

    if request.method == 'POST':
        # Update the order with the new values from the form
        order.fname = request.POST.get('fname')
        order.lname = request.POST.get('lname')
        order.company_name = request.POST.get('company_name')
        order.country = request.POST.get('country')
        order.street_address = request.POST.get('street_address')
        order.postcode = request.POST.get('postcode')
        order.city = request.POST.get('city')
        order.phone = request.POST.get('phone')
        order.email = request.POST.get('email')
        order.order_note = request.POST.get('order_note')
        order.payment_method = request.POST.get('payment_method')
        order.status = request.POST.get('status')

        # Save the updated order
        order.save()

        # Redirect to the order list page after updating
        return redirect('seller:orders_list')

    return render(request, 'seller/order_update.html', {'order': order})

# View to delete an order
def order_delete(request, orderid):
    order = get_object_or_404(Order, orderid=orderid)
    if request.method == 'POST':
        order.delete()
        return redirect('seller:orders_list')
    return render(request, 'seller/order_delete.html', {'order': order})

def users_list(request):
    users = UserProfile.objects.all()
    return render(request, 'seller/users_list.html', {'users': users})

# View to edit a user's information (optional)
def user_update(request, userid):
    user = get_object_or_404(UserProfile, userid=userid)
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')
        user.address = request.POST.get('address')
        user.gender = request.POST.get('gender')
        user.save()
        return redirect('seller:users_list')
    return render(request, 'seller/user_update.html', {'user': user})

# View to delete a user (optional)
def user_delete(request, userid):
    user = get_object_or_404(UserProfile, userid=userid)
    if request.method == 'POST':
        user.delete()
        return redirect('seller:users_list')
    return render(request, 'seller/user_delete.html', {'user': user})


def feedbacks_list(request):
    s = SellerPerson.objects.get(email=request.session['ven_email'])
    s_id = s.id
    feedbacks = feedback.objects.filter(product__seller_id=s_id)
    return render(request, 'seller/feedbacks_list.html', {'feedbacks': feedbacks})


def sub_category_one_list(request):
    sub_category_ones = sub_category_one.objects.all()
    return render(request, 'seller/sub_category_one_list.html', {'sub_category_ones': sub_category_ones})

# View to update a sub_category_one
def sub_category_one_update(request, id):
    subcat_one = get_object_or_404(sub_category_one, id=id)
    if request.method == 'POST':
        subcat_one.name = request.POST.get('name')
        subcat_one.save()
        return redirect('seller:sub_category_one_list')
    return render(request, 'seller/sub_category_one_update.html', {'subcat_one': subcat_one})

# View to delete a sub_category_one
def sub_category_one_delete(request, id):
    subcat_one = get_object_or_404(sub_category_one, id=id)
    if request.method == 'POST':
        subcat_one.delete()
        return redirect('seller:sub_category_one_list')
    return render(request, 'seller/sub_category_one_delete.html', {'subcat_one': subcat_one})


# View to show all sub_category
def sub_category_list(request):
    sub_categories = sub_category.objects.all()
    return render(request, 'seller/sub_category_list.html', {'sub_categories': sub_categories})

# View to update a sub_category
def sub_category_update(request, id):
    # Get the subcategory that needs to be updated
    subcat = get_object_or_404(sub_category, id=id)

    # Fetch all categories and sub_category_ones to display in the form
    categories = category.objects.all()
    sub_category_ones = sub_category_one.objects.all()

    if request.method == 'POST':
        form = SubCategoryForm(request.POST)
        if form.is_valid():
            # Update the subcategory with the new data
            subcat.name = form.cleaned_data['name']
            subcat.category = form.cleaned_data['category']
            subcat.sub_category_one = form.cleaned_data['sub_category_one']
            subcat.save()
            return redirect('seller:sub_category_list')  # Redirect to the list page
    else:
        # Initialize form with current subcategory data
        form = SubCategoryForm(initial={
            'name': subcat.name,
            'category': subcat.category,
            'sub_category_one': subcat.sub_category_one
        })

    return render(request, 'seller/sub_category_update.html', {
        'form': form,
        'subcat': subcat,
        'categories': categories,
        'sub_category_ones': sub_category_ones,
    })

# View to delete a sub_category
def sub_category_delete(request, id):
    subcat = get_object_or_404(sub_category, id=id)
    if request.method == 'POST':
        subcat.delete()
        return redirect('seller:sub_category_list')
    return render(request, 'seller/sub_category_delete.html', {'subcat': subcat})


def sub_category_one_add(request):
    if request.method == 'POST':
        form = SubCategoryOneForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('seller:sub_category_one_list')
    else:
        form = SubCategoryOneForm()
    return render(request, 'seller/sub_category_one_add.html', {'form': form})


def sub_category_add(request):
    if request.method == 'POST':
        form = SubCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('seller:sub_category_list')
    else:
        form = SubCategoryForm()
    return render(request, 'seller/sub_category_add.html', {'form': form})

def delete_cat(request, id):
    cat = category.objects.get(id=id)
    cat.delete()
    return redirect('seller:shop')


def delete_prod(request, id):
    p = product.objects.get(product_id=id)
    p.delete()
    return redirect('seller:shop')

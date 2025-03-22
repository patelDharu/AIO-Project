from django.shortcuts import render, redirect
from User.models import *
from .models import *
from django.contrib import messages 

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


def edit_cat(request,id):
    cat = category.objects.get(id = id)
    if request.method == 'POST':
        cat.name = request.POST['cname']
        # cat.image = request.FILES['image']
        if 'image' in request.FILES:
            cat.image = request.FILES['image']
        cat.save()
        return render(request,"seller/add_cat.html",{'cat':cat})
    else:
        return render(request,"seller/add_cat.html",{'cat':cat})

def add_cat(request):
    if request.method == "POST":
        name = request.POST.get('cname')
        image = request.FILES.get('image')

        new_category = category(name=name, image=image)
        new_category.save()

        return redirect('seller:shop')
    return render(request,"seller/add_cat.html")

def edit_prod(request,id):
    pro = product.objects.get(product_id = id)
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

        # Handle updating the size (assuming one size is selected)
        size_selected = request.POST.get('size')
        selected_size = Size.objects.get(id=size_selected)
        pro.sizes.clear()  # Clear previous sizes (if any)
        pro.sizes.add(selected_size)  # Add the new size

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

        # Handle saving the size (assuming only one size is selected)
        size_selected = request.POST.get('size')  # Get the selected size (only one option in this case)
        selected_size = Size.objects.get(id=size_selected)
        new_product.sizes.add(selected_size)  # Add the size to the many-to-many relationship

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


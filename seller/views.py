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
        cat = category.objects.all()
        pro = product.objects.all()
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
    return render(request,"seller/add_cat.html")

def edit_prod(request,id):
    pro = product.objects.get(product_id = id)
    sub_cat = sub_category.objects.all()
    return render(request,"seller/add_prod.html",{'pro':pro,'sub_cat':sub_cat})

def add_prod(request):
    sub_cat = sub_category.objects.all()
    return render(request,"seller/add_prod.html",{'sub_cat':sub_cat})


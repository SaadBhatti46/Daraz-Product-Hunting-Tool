from django.shortcuts import render, redirect
from tablib import Dataset

from .decorators import unauthenticated_user , allowed_users , admin_only
from .forms import UserForm, ProfileForm
from .models import *
import uuid
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .resources import ProductResources
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required

# Create your views here.
def is_valid_queryparam(param):
    return param != '' and param is not None


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def SimpleUpload(request):
    if request.method == 'POST':
        product_resources = ProductResources()
        dataset = Dataset()
        new_product = request.FILES['myFile']
        #
        # if not new_product.name.endswith['xlsx']:
        #     messages.info(request,'wrong format')
        #     return render(request,'upload.html')
        imported_data = dataset.load(new_product.read(), format='xlsx')
        # print(imported_data)
        for data in imported_data:
            print(data[1])
            value = Product(
                data[0], data[1], data[2], data[3], data[4], data[5], data[6],
                data[7], data[8], data[9], data[10], data[11], data[12], data[13], data[14])
            value.save()
    return render(request, 'upload.html')


@login_required(login_url='login')
def ProductInfo(request):
    productdetail = Product.objects.all()
    return render(request, 'product.html', {'productdetail': productdetail})


def SellerTracking(request):
    productdetail = Product.objects.all()
    return render(request, 'tracking.html', {'productdetail': productdetail})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def ShowSellerDataToAdmin(request):
    super_user = request.user
    if super_user.is_superuser:
        SellerData = User.objects.all()
        return render(request, 'seller.html', {'seller': SellerData})
    else:
        messages.success(request, "Not Authorized")
        return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def SellerDeleteByAdmin(request, id):
    if request.method == 'POST':
        SellerId = User.objects.get(pk=id)
        SellerId.delete()
        messages.success(request, "Seller " + SellerId.username + " Deleted")
        return redirect('seller')
    else:
        return redirect('seller')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def SellerDataUpdateByAdmin(request, id):
    if request.method == 'POST':
        SellerId = User.objects.get(pk=id)
        username = request.POST.get('username')
        email = request.POST.get('email')
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')

        if is_valid_queryparam(username):
            if User.objects.filter(username=username).first():
                messages.success(request, "Username Taken")
                return redirect(f'/update/{id}')
            else:
                SellerId.username = username

        if is_valid_queryparam(email):
            if User.objects.filter(email=email).first():
                messages.success(request, "Email Taken")
                return redirect(f'/update/{id}')
            else:
                SellerId.email = email

        if is_valid_queryparam(firstname):
            SellerId.first_name = firstname

        if is_valid_queryparam(lastname):
            SellerId.last_name = lastname

        SellerId.save()
        messages.success(request, "Seller " + SellerId.username + " Record Updated")
        return redirect('seller')

    return render(request, "update.html")


@login_required(login_url='login')
def Search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        product = Product.objects.filter(productLink__contains=searched)
        return render(request, 'search.html', {'product': product})
    else:
        return render(request, 'search.html')


@login_required(login_url='login')
def MultiSearch(request):
    if request.method == "POST":
        # Product.objects.all().delete()
        brand_value = request.POST.get('brand')
        rating_value = request.POST.get('rating')
        stock_value = request.POST.get('stock')
        sale_value = request.POST.get('sale')
        price_value = request.POST.get('price')

        if is_valid_queryparam(brand_value) and is_valid_queryparam(rating_value) and is_valid_queryparam(
                stock_value) and is_valid_queryparam(sale_value):
            qu = Product.objects.raw(
                'select * from daraz_product where brand="' + brand_value + '" and rating>="' + rating_value + '" and stock>="' + stock_value + '" and sales>="' + sale_value + '"')
            return render(request, 'multiplesearch.html', {'product': qu})
        elif is_valid_queryparam(brand_value) and is_valid_queryparam(rating_value) and is_valid_queryparam(
                stock_value):
            qu = Product.objects.raw(
                'select * from daraz_product where brand="' + brand_value + '" and rating>="' + rating_value + '" and stock>="' + stock_value + '"')
            return render(request, 'multiplesearch.html', {'product': qu})
        elif is_valid_queryparam(brand_value) and is_valid_queryparam(rating_value) and is_valid_queryparam(sale_value):
            qu = Product.objects.raw(
                'select * from daraz_product where brand="' + brand_value + '" and rating>="' + rating_value + '" and sales>="' + sale_value + '"')
            return render(request, 'multiplesearch.html', {'product': qu})
        elif is_valid_queryparam(brand_value) and is_valid_queryparam(stock_value) and is_valid_queryparam(sale_value):
            qu = Product.objects.raw(
                'select * from daraz_product where brand="' + brand_value + '" and stock>="' + stock_value + '" and sales>="' + sale_value + '"')
            return render(request, 'multiplesearch.html', {'product': qu})
        elif is_valid_queryparam(rating_value) and is_valid_queryparam(sale_value) and is_valid_queryparam(stock_value):
            qu = Product.objects.raw(
                'select * from daraz_product where rating>="' + rating_value + '" and sales>="' + sale_value + '" and stock>="' + stock_value + '"')
            return render(request, 'multiplesearch.html', {'product': qu})
        elif is_valid_queryparam(rating_value) and is_valid_queryparam(sale_value):
            qu = Product.objects.raw(
                'select * from daraz_product where rating>="' + rating_value + '" and sales>="' + sale_value + '"')
            return render(request, 'multiplesearch.html', {'product': qu})
        elif is_valid_queryparam(rating_value) and is_valid_queryparam(stock_value):
            qu = Product.objects.raw(
                'select * from daraz_product where rating>="' + rating_value + '" and stock>="' + stock_value + '"')
            return render(request, 'multiplesearch.html', {'product': qu})
        elif is_valid_queryparam(sale_value) and is_valid_queryparam(stock_value):
            qu = Product.objects.raw(
                'select * from daraz_product where sales>="' + sale_value + '" and stock>="' + stock_value + '"')
            return render(request, 'multiplesearch.html', {'product': qu})
        elif is_valid_queryparam(brand_value) and is_valid_queryparam(rating_value):
            qu = Product.objects.raw(
                'select * from daraz_product where brand="' + brand_value + '" and rating>="' + rating_value + '"')
            return render(request, 'multiplesearch.html', {'product': qu})
        elif is_valid_queryparam(brand_value) and is_valid_queryparam(stock_value):
            qu = Product.objects.raw(
                'select * from daraz_product where brand="' + brand_value + '" and stock>="' + stock_value + '"')
            return render(request, 'multiplesearch.html', {'product': qu})
        elif is_valid_queryparam(brand_value) and is_valid_queryparam(sale_value):
            qu = Product.objects.raw(
                'select * from daraz_product where brand="' + brand_value + '" and sales>="' + sale_value + '"')
            return render(request, 'multiplesearch.html', {'product': qu})
        elif is_valid_queryparam(brand_value):
            qu = Product.objects.filter(brand=brand_value)
            return render(request, 'multiplesearch.html', {'product': qu})
        elif is_valid_queryparam(rating_value):
            qu = Product.objects.filter(rating__gte=rating_value)
            return render(request, 'multiplesearch.html', {'product': qu})
        elif is_valid_queryparam(stock_value):
            qu = Product.objects.filter(stock__gte=stock_value)
            return render(request, 'multiplesearch.html', {'product': qu})
        elif is_valid_queryparam(sale_value):
            qu = Product.objects.filter(sales__gte=sale_value)
            return render(request, 'multiplesearch.html', {'product': qu})
        # elif is_valid_queryparam(price_value):
        #     qu = Product.objects.filter(price__gte=price_value)
        #     return render(request, 'daraz/multiplesearch.html', {'product': qu})

        else:
            return render(request, 'multiplesearch.html')
    else:
        return render(request, 'multiplesearch.html')




# def sidebar(request):
#     return  render(request, 'base_sidebar.html')
#
@login_required(login_url='login')
def dashboard(request):
    all = User.objects.all()
    total_user = all.count()
    # totals products
    productdetail = Product.objects.all()
    total_product = productdetail.count()
    context = {'total_user': total_user, 'total_product': total_product, 'all_pro': productdetail}
    return render(request, 'dashboard.html', context)
    # return  render(request, 'dashboard.html')


# @login_required(login_url='/')
# @allowed_users(allowed_roles=['seller'])
# def userPage(request):
#     context = {}
#     return render(request , 'user.html', context)

@login_required(login_url='login')
def ProductInfo(request):
    productdetail = Product.objects.all()
    return render(request, 'product.html', {'productdetail': productdetail})


@unauthenticated_user
def SignUp(request):

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        try:
            if User.objects.filter(username=username).first():
                messages.success(request, "Username Taken")
                return redirect('signup')

            if User.objects.filter(email=email).first():
                messages.success(request, "Email Taken")
                return redirect('signup')

            if len(password1) < 8 and len(password2) < 8:
                messages.success(request, "Password Lenght Minimum 8")
                return redirect('signup')

            if password1 != password2:
                messages.success(request, "Password Not Matched")
                return redirect('signup')

            user_obj = User.objects.create(username=username, email=email, first_name=firstname, last_name=lastname)
            user_obj.set_password(password1)
            user_obj.save()
            group = Group.objects.get(name='seller')
            user_obj.groups.add(group)
            auth_token = str(uuid.uuid4())

            profile_obj = Profile.objects.create(user=user_obj, auth_token=auth_token)
            profile_obj.save()
            SendMail(email, auth_token)
            messages.success(request, "Verification Email Has Been Sent To Your Mail")
            return redirect('signup')

        except Exception as e:
            print(e)

    return render(request, 'signup.html')


# @login_required(login_url='login')
def SendMail(email, token):
    subject = "ASAN BUSINESS ACCOUNT VERIFICATION"
    message = f'Hi Click The Link To Verify Your Account \n\n http://127.0.0.1:8000/accountverify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


# @login_required(login_url='login')
def AccountVerify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, "Account Already Verified")
                return redirect('login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, "Your Account Has Been Verified")
            return redirect('login')
        else:
            return redirect('signup')
    except Exception as e:
        messages.success(request, e)
        return redirect('signup')

@unauthenticated_user
def LoginUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=username).first()

        if user_obj is None:
            messages.success(request, "User Doesn't Exists")
            return redirect('login')

        profile_obj = Profile.objects.filter(user=user_obj).first()

        if not user_obj.is_superuser:
            if not profile_obj.is_verified:
                messages.success(request, "Profile not verified Check your mail")
                return redirect('login')

        user = authenticate(username=username, password=password)

        if user is None:
            messages.success(request, "Wrong Password")
            return redirect('login')

        login(request, user)
        return redirect('dashboard')

    return render(request, 'signin.html')


def Forget(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')

            if not User.objects.filter(username=username).first():
                messages.success(request, "User Doesn't Exists")
                return redirect('forgetpassword')

            user_obj = User.objects.get(username=username)
            token = str(uuid.uuid4())
            profile_obj = Profile.objects.get(user=user_obj)
            profile_obj.auth_token = token
            profile_obj.save()
            SendForgetPasswordMail(user_obj.email, token)
            messages.success(request, "An Email is sent")
            return redirect('forgetpassword')

    except Exception as e:
        print(e)
    return render(request, 'forget.html')


def ChangePassword(request, token):
    context = {}
    try:
        profile_obj = Profile.objects.filter(auth_token=token).first()
        context = {'user_id': profile_obj.user.id}

        if request.method == 'POST':
            new_password = request.POST.get('password1')
            confirm_password = request.POST.get('password2')
            user_id = request.POST.get('user_id')

            if user_id is None:
                messages.success(request, "User ID not found")
                return redirect(f'/changepassword/{token}/')

            if new_password != confirm_password:
                messages.success(request, "Password Should Be Equal")
                return redirect(f'/changepassword/{token}/')

            if len(new_password) < 8 or len(confirm_password) < 8:
                messages.success(request, "Password Lenght Minimum 8")
                return redirect(f'/changepassword/{token}/')

            user_obj = User.objects.get(id=user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('login')

    except Exception as e:
        print(e)
    return render(request, 'changepassword.html', context)


def SendForgetPasswordMail(email, token):
    subject = "Forget Password Mail"
    message = f'Hi, Click on link to reset your password \n\n http://127.0.0.1:8000/changepassword/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)

def LogoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def profit_cal(request):
    p = ""
    if request.method == "POST":
        sel = request.POST.get('sel_price')
        cost = request.POST.get('cost_price')
        shiping = request.POST.get('shipping_price')
        flyer = request.POST.get('Flyer_price')
        vat = request.POST.get('vat')
        category = request.POST.get('category')


        category = float(category)
        print(category)

        vat = float(vat)
        print(vat)
        sel = float(sel)
        cost = float(cost)
        shiping = float(shiping)
        flyer = float(flyer)

        dc = float(category * sel) / 100
        print(dc)

        vat_comission = float(vat * dc) / 100
        print(vat_comission)

        pay_fee = float(1.25 * sel) / 100
        print(pay_fee)

        vat_paymentfee = float(16 * pay_fee) / 100
        print(vat_paymentfee)

        vat_shipping_fee = float(shiping * 16) /100
        print(vat_shipping_fee)

        flyer_chrg = flyer

        daraz_comission = float(dc + vat_comission + pay_fee + vat_paymentfee + vat_shipping_fee + flyer_chrg)
        print(daraz_comission)

        profit = float(sel - cost - daraz_comission)
        print(profit)

        prfper = float(profit * 100) / sel
        # prf_per = str(prf_per)
        print(prfper)

        p = prfper

        # context = {'dc': prf_per}

    return render(request, 'profit_calculator.html', {'profit': p})

def landing_page(request):

    if request.method == "POST":
        name = request.POST.get('name')
        em = request.POST.get('email')
        sub = request.POST.get('sub')
        msg = request.POST.get('msg')

        subject = "Contact Support Mail-No reply"
        message = f'USER-Details\n\n Name : '+name+' \n Email : '+em+'\n Subject : '+sub+'\n Issue : '+msg
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['pythonpractice00@gmail.com']
        send_mail(subject, message, email_from, recipient_list)
        #
        messages.success(request, "Email Send Successfully to our Team.Thanks, We will get back to you soon.")

    return render(request, 'landing_page.html')

@login_required(login_url='login')
def accountSettings(request):
    user = request.user
    profile = Profile.objects.filter(user = user).first()
    userform = UserForm(instance=user)
    profileform = ProfileForm(instance=profile)

    if request.method == 'POST':
        userform = UserForm(request.POST,instance=user)
        image = request.FILES.get('image')

        # profileform = ProfileForm(request.POST, request.FILES,instance=profile)
        # print(profileform)
        print('Hi Hello')
        if image is None:
            if userform.is_valid():
                userform.save()
        else:
            profile.profile_pic = image
            profile.save()
            if userform.is_valid():
                userform.save()

        # if profileform.is_valid():
        #     profileform.save()


    context = {'form':userform , 'pic':profileform}
    return render(request, 'account_settings.html', context)




# Contact
@login_required(login_url='login')
@allowed_users(allowed_roles=['seller'])
def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        em = request.POST.get('em')
        sub = request.POST.get('sub')
        msg = request.POST.get('msg')

        subject = "Contact Support Mail-No reply"
        message = f'USER-Details\n\n Name : '+name+' \n Email : '+em+'\n Subject : '+sub+'\n Issue : '+msg
        # message = f'USER-Details\n\n Issue : ' + sub + '\n\n Message : ' + msg
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['pythonpractice00@gmail.com']
        send_mail(subject, message, email_from, recipient_list)
        #
        messages.success(request, "Email Send Successfully to our Team.Thanks, We will get back to you soon.")


    return render(request, "contact.html")
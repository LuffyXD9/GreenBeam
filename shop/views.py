
from ast import And

from email import message
from re import A
from django.db.models.fields import CommaSeparatedIntegerField
# from numpy import product
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.models import User
from math import ceil
import json
import io
from datetime import date
from django.contrib import messages
from yaml import load

from AP.settings import MEDIA_ROOT

from turtle import clear, update
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product,Contact, Order, OrderUpdate, Cartrecord






# Create your views here.
def loadAllProducts(): 
    allProds = []
    catprods = Product.objects.values('category')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n//4 + ceil((n/4)-(n//4))
        allProds.append([prod, range(1, nSlides), nSlides])
    return {'allProds': allProds}




def index(request):
    params = loadAllProducts()
    return render(request, 'shop/index.html', params)


def signUp(request):
    flag = 0
    if(request.method=='POST'):
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        currentPath = request.POST['currentPathsignIn']

        if len(username)<3 or len(username)>20:
            messages.warning(request, 'Username is either too long or too short')
            flag=1

        if not username.isalnum():
            messages.warning(request, 'Username should contain either alphabets or numerics')
            flag=1

        if pass1!=pass2:
            messages.warning(request, 'Password is not matching')
            flag=1

        if User.objects.filter(username = username).first():
            messages.error(request, "This username is already taken")    
            flag=1

        if flag==1:
            return redirect(currentPath)

        else:
            myuser = User.objects.create_user(username, email, pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()
            messages.success(request, "your account has been successfully created")
            login(request,myuser)
            return redirect(currentPath)
             
    else:
        return HttpRequest("404 - Not found")    



def userlogin(request):
    if(request.method=='POST'):
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']
        currentPathlogIn=request.POST['currentPathlogIn']

        user = authenticate(username = loginusername, password = loginpass )

        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully Logged In')
            return redirect(currentPathlogIn)
        else:
            messages.error(request, 'Invalid credentials, Please try again')
            return redirect(currentPathlogIn)
    return HttpResponse('404 - Not found')

def userlogout(request):
    if request.method == 'POST':
        logoutcurrentPath = request.POST['logoutcurrentPath']
    logout(request)
    messages.error(request, 'Successfully Logged Out')
    return redirect(logoutcurrentPath)


def about(request):
    return render(request, 'shop/about.html')
    


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name = name, email = email, phone = phone, desc = desc)
        contact.save()
        messages.success(request, "Thank you for contacting us, we will get back to you as soon as possible.")
    return render(request, 'shop/contact.html')



def tracker(request): 
    params={}
    if request.user.is_authenticated:
        orders_list=[]
        checkout=Order.objects.filter(user=request.user)
        print(checkout)
        if len(checkout)>0:
            for order in checkout:
                track = OrderUpdate.objects.filter(user=request.user,order_id=order.order_id).order_by('timestamp')
                orders_list.append([order,track])
                print(orders_list);
            params['order_list'] = orders_list
    return render(request, "shop/tracker.html",params)
    

def search(request):
        gun = 0
        key=request.POST.get('search')
        if(key==None or key.split()==[]):
            messages.error(request,'Please enter valid keywords')
            params=loadAllProducts()
        else:
            allProds = []
            catprods = Product.objects.values('category')
            cats = {item['category'] for item in catprods}
            for j in cats:
                if key.lower() == j.lower():
                    search_item = Product.objects.filter(category=key)
                    gun = 1
            if(gun==0):
                allProname= Product.objects.filter(product_name__icontains=key)
                allProsubcat= Product.objects.filter(subcategory__icontains=key)
                allProdesc =Product.objects.filter(desc__icontains=key)
                search_item =  allProname.union(allProsubcat, allProdesc)

            n = search_item.count()
            if(n!=0):

                nSlides = n//4 + ceil((n/4)-(n//4))
                allProds.append([search_item, range(1, nSlides), nSlides])


            if(len(allProds)==0):
                messages.error(request,'No match found, Please try different keyword')
                params = loadAllProducts()
                return render(request, 'shop/index.html',params)
            params = {'allProds': allProds}
        return render(request, "shop/index.html", params)






def productView(request, myid):
    p ={}
    qvprods = Product.objects.filter(id=myid)
    exo = myid
    p['qvprods']=qvprods[0]
    p['exo']=exo
    print(p)
    return render(request, 'shop/productView.html',p )



def checkout(request):
    
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        if(len(items_json)>3):
            order = Order(user=request.user,items_json=items_json, name=name, email=email, address=address, city=city,
                        state=state, zip_code=zip_code, phone=phone)
        
            today = date.today()
            order_date = today.strftime("%b-%d-%Y")
            order.items_json = order.items_json[:-1] + ''',"date":["'''f"{order_date}"'''"]}'''
            order.save()

            update = OrderUpdate(order_id = order.order_id,user=request.user, update_desc = "The order has been placed,Track your Order using My order.")
            update.save()

            #erasing the cart data after sucessfully placing the order 
            cart_record=Cartrecord.objects.get(cart_user=request.user)
            cart_record.json_data="0"
            cart_record.save()

            messages.success(request, 'Order placed successfully, track your order using My order.Thank you for shopping')
            cartClear = True
            return render(request, 'shop/checkout.html',{'cartClear':cartClear})
        else:
             messages.error(request, 'Your cart is Empty!')
    # params=load_cart(request,params)
    return render(request, "shop/checkout.html")
    


@csrf_exempt
def timestamp(request):
    if request.method=="POST":
        if request.user.is_authenticated:
            json_cart_data=request.body
            print(json_cart_data)
            stream=io.BytesIO(json_cart_data)
            print(stream)
            json_cart_object=JSONParser().parse(stream)
            print(json_cart_object)
            json_cart_string=json.dumps(json_cart_object)
            print(json_cart_string)
            try:
                cart_object=Cartrecord.objects.get(cart_user=request.user)
                cart_object.json_data=json_cart_string
                cart_object.save()
            except:
                cart_object=Cartrecord(cart_user=request.user)
                cart_object.save()
    return HttpResponse("successfully updated")
from django.shortcuts import render,redirect
from .models import Product, Contact, Order, OrderUpdate,Customer
from math import ceil
import json,random,math
from django.http import HttpResponse
from django.core.mail import send_mail
from instamojo_wrapper import Instamojo



# function for index---------------------------------------------------------------------------------------------
def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds}
    return render(request, 'shop/index.html', params)

# for about us page----------------------------------------------------------------------------------------------
def about(request):
    return render(request, 'shop/about.html')

# function for contact page-----------------------------------------------------------------------------------------
def contact(request):
    if request.method=="POST":
        if request.session.get("customer_id"):
            name = request.POST.get('name', '')
            email = request.POST.get('email', '')
            phone = request.POST.get('phone', '')
            desc = request.POST.get('desc', '')
            contact = Contact(name=name, email=email, phone=phone, desc=desc)
            contact.save()
        else:
            return render(request,"shop/login.html")
    return render(request, 'shop/contact.html')

# function for tracking----------------------------------------------------------------------------------------
def tracker(request):
    if request.method=="POST":
        if request.session.get("email"):
            orderId = request.POST.get('orderId', '')
            try:
                cust_email=request.session.get("email")
                order = Order.objects.filter(order_id=orderId, email=cust_email)
                if len(order)>0:
                    update = OrderUpdate.objects.filter(order_id=orderId) 
                    return render(request,"shop/tracker.html",{"updates":update,"order":order})
                else:
                    return render(request,"shop/tracker.html",{"msg":"There is no order associated with this order id"})   
            except:
                return render(request,"shop/tracker.html",{"msg":"There is no order associated with this order id"})  
        else:
            return render(request,"shop/tracker.html",{"login":"Please login to continue"})         

    else:
        return render(request, "shop/tracker.html")

# for search template------------------------------------------------------------------------------------------------
def search(request):
    return render(request, 'shop/search.html')

def productView(request, myid):
    # Fetch the product using the id
    product = Product.objects.filter(id=myid)
    return render(request, 'shop/prodView.html', {'product':product[0]})

# function for checkout-------------------------------------------------------------------------------
def checkout(request):    
    if request.method=="POST":
        amount = request.POST.get('amount')        
        if str(amount)!="0":
            
            if request.session.get("customer_id"):
                cust_email=request.session.get("email")
                items_json = request.POST.get('itemsJson', '')
                
                name = request.POST.get('name', '')
                amount = request.POST.get('amount', '')
                email = request.POST.get('email', '')
                address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
                city = request.POST.get('city', '')
                state = request.POST.get('state', '')
                zip_code = request.POST.get('zip_code', '')
                phone = request.POST.get('phone', '')
                details={"items_json":items_json,"cust_email":cust_email,"items_json":items_json,"name":name,"email":email,"address":address,"city":city,"state":state,"zip_code":zip_code,"phone":phone,"amount":amount}
                return render(request,"shop/payment.html",details)
            else:
                return render(request,"shop/login.html")   
        else:
            return render(request,"shop/checkout.html",{"alert":"Please add atleast one item in your Cart"})
            
    
    return render(request, 'shop/checkout.html')

# order payment
def payhandler(request):
    if request.method=="POST":
        cust_email = request.POST.get('cust_email')
        items_json = request.POST.get('items_json')      
        nameorder = request.POST.get('nameorder')
        emailorder = request.POST.get('emailorder')
        address = request.POST.get('address')
        landmark = request.POST.get('landmark')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        phone = request.POST.get('phone')
        amountorder = request.POST.get('amountorder')  
        # _________________________________________________
        name = request.POST.get('name')
        purpose = request.POST.get('purpose')
        email = request.POST.get('email')
        amount = request.POST.get('amount')
        print(name,purpose,email,amount)
        API_KEY = "test_1a3a4dfe51644a092dca2fa5e47"
        AUTH_TOKEN = "test_5ede1870ea6ffd3a802912f8b4e"
        api = Instamojo(api_key=API_KEY,auth_token=AUTH_TOKEN,endpoint='https://test.instamojo.com/api/1.1/')
        
        response = api.payment_request_create(
        amount=amount,
        purpose=purpose,
        buyer_name=name,
        send_email=True,
        email=email,
        redirect_url="http://localhost:8000/shop/status")
        order = Order(items_json=items_json, name=name, email=email, address=address, city=city,
                           state=state, zip_code=pincode, phone=phone,amount=amount,cust_details=cust_email)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="Your order has been placed")
        update.save()
        
        
        
        
        return redirect(response['payment_request']['longurl'])
    
    else:
        
        return redirect('/shop/checkout')
    
# payment status
def status(request):
    return render(request,"shop/status.html")
    

# function for search functionality---------------------------------------------------------------
def search(request):
    query= request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod=[item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod)!= 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg":""}
    if len(allProds)==0 or len(query)<4:
        params={'msg':"Enter a valid Search"}
    return render(request, 'shop/search.html', params)


def searchMatch(query, item):
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False
    
    
    # otp function
def generateOTP() :
    digits = "0123456789"
    OTP = ""
    for i in range(4) :
        OTP += digits[math.floor(random.random() * 10)]
    return OTP

# function for signup---------------------------------------------------------------------------------------
def signup(request):
    flag=""
    if request.method=="POST":
        
        pdata=request.POST.get
        fname=pdata("firstname")
        lname=pdata("lastname")
        email=pdata("email")
        phone=pdata("phone")
        password1=pdata("password1")
        password2=pdata("password2")

        form=Customer.objects.all()
        for i in form:
            if i.email==email or i.phone==phone:
                flag=True
        if flag:
            alert="user already exist with this mobile number"
        elif not flag:
            if password1!= password2:
                alert="password didnot match"
            else:
                Customer(firstname=fname,lastname=lname,email=email,phone=phone,password=password1).save()
                # request.session["email"] = email
                return redirect("/shop/login")
                
                alert="Registration Successful"

        return render(request,"shop/signup.html",{"alert":alert ,"first_name":fname,"last_name":lname,"email":email,"phone":phone})
    else:

        return render(request,"shop/signup.html")
    
    # verifyotp
def verifyotp(request):
    if request.method=="POST":
        pdata=request.POST.get
        email=pdata("email1")
        otpsystem=pdata("otp")
        userotp=pdata("otpbackend")
        if otpsystem==userotp:
            return render(request,"shop/signup.html",{"email":email})
        else:
            return render(request,"shop/reg.html",{"msg":"Sorry Otp was incorrect"})
    else:
        return redirect("/reg")
        
        
    
    
    
    # otpsend
def reg(request):
    if request.method=="POST":
        email=request.POST.get("email")
        obj=Customer.objects.filter(email=email)
        if obj.exists():
            return render(request,"shop/reg.html",{"msg":"Email already exist"})
        else:
            o=generateOTP()
            print(o)
            htmlgen = "<p> Your OTP is </p>"  +  " " "<strong>" + str(o)  + "</strong>"
            # send_mail('E-mail verification',o,'webshopee11@gmail.com',[email], fail_silently=False, html_message=htmlgen)
            
            return render(request,"shop/reg.html",{"get_email":email,"otp":o})
    else:
        return render(request,"shop/reg.html")
    
    
    
    
    
    


# function for login---------------------------------------------------------------------------------
def login(request):
    form=""
    flag=""
    if request.method=="POST":
        pdata = request.POST.get

        credential = pdata("text")
        password1 = pdata("password1")
        form = Customer.objects.all()
        for i in form:
            if (i.email==credential or i.phone==credential) and password1==i.password:
                flag=True
                cid=i.id
                cemail=i.email
                fname=i.firstname
                lname=i.lastname
                phone=i.phone

        if  flag:
            alert="Login Success"
            print("login success")
            flag=True
            request.session["customer_id"]=cid
            request.session["email"] = cemail
            request.session["fname"] = fname
            request.session["lname"] = lname
            request.session["phone"] = phone

            return redirect( "/shop", {"alert": alert,"flag":flag,"fname":fname})

        else:
                alert="Invalid Credentials"

                return render(request,"shop/login.html",{"alert":alert,"credential":credential})
    else:
        return render(request, "shop/login.html")

# views for logout----------------------------------------------------------------------------------
def logout(request):
    
    request.session.clear()
    return redirect("/shop/login",{"msg":"clear_session"})

# views for profile________________________________________________________________________________________

def profile(request):
    fname=request.session.get("fname")
    lname=request.session.get("lname")
    email=request.session.get("email")
    phone=request.session.get("phone")
    return render(request,"shop/profile.html",{"fname":fname,"lname":lname,"email":email,"phone":phone})

# views for orders______________________________________________________________________________________________
def orders(request):
    
    cust_email = request.session.get("email")
    print(cust_email)
    if request.session.get("customer_id"):

        try:
            cust_orders=Order.objects.filter(cust_details=cust_email)
            print(cust_orders)
            if cust_orders:
              data={"order_fetch":cust_orders}
              return render(request,"shop/orders.html",data)
            else:
              return render(request,"shop/no_order.html")
                
                # return render(request, "shop/orders.html", {"order_fetch":"No Orders Found"})

        except:
            return render(request,"shop/no_order.html")
     
                # return render(request,"shop/orders.html",{"order_fetch":"No Orders Found"})


# ________________________________________________________________________________
def chatbot(request):
    return render(request,"shop/chatroom.html")
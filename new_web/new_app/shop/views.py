from django.http.response import HttpResponse
from django.shortcuts import render,HttpResponse,redirect
from .models import Product,Orders,OrderUpdate,ProductComment,Contact
import json
import ast
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,  login, logout
from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum
from django.contrib import messages 

from django.core.paginator import Paginator


MERCHANT_KEY = 'Your-Merchant-Key-Here'

def index(request):
    products = Product.objects.filter(category='trending')[0:10]
    sliPro = Product.objects.all()[:20]
    params = {'allProds':products,'sliPro':sliPro}
    return render(request, 'index.html', params)

def shop(request,slug=None):
    catprods = Product.objects.values('category', 'product_id')
    cats = {item['category'] for item in catprods}
    if slug == None:
        products = Product.objects.all()
        paginator = Paginator(products,2)
        page_number = request.GET.get('page')
        products = paginator.get_page(page_number)
        params = {'allProds':products,'cats':cats}
        return render(request, 'shop.html', params)
    products = Product.objects.filter(category=slug)
    paginator = Paginator(products,2)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    print(type(products))
    params = {'allProds':products,'cats':cats}
    return render(request, 'shop.html', params)

def Contact_(request):
    if request.method == "POST":
        email = request.POST.get('email')
        message = request.POST.get('msg')
        contact = Contact(email = email,message = message)
    return render(request,'contact.html')
def About(request):
    return render(request,'about.html')

def Search(request):
    if request.method == "POST":
        query=request.POST.get('query')
        if len(query)>78:
            allPro=Product.objects.none()
        else:
            allProName= Product.objects.filter(product_name__icontains=query)
            allProDesc= Product.objects.filter(desc__icontains=query)
            allProCate =Product.objects.filter(category__icontains=query)
            allPro=  allProName.union(allProDesc, allProCate)
        if allPro.count()==0:
            messages.warning(request, "No search results found. Please refine your query.")
        params={'allPro': allPro, 'query': query}
        return render(request, 'search.html', params)
    return render(request,'home.html')

def Login(request):
    return render(request,'login.html')


# displaying a single element and adding 'Add to Cart' functionality
def product_view(request,my_id):
    product = Product.objects.filter(product_id=my_id)
    colors = (str(product[0].colors).split(','))
    sizes = str(product[0].Sizes).split(',')
    comments= ProductComment.objects.filter(product = product[0])
    
    if request.method == 'POST':
        cart_item = True
        oper = request.POST.get('operation')
        if oper == "2":
            product_id = request.POST.get('product')
            product_image = Product.objects.filter(product_id=product_id)[0].image
            product_price = Product.objects.filter(product_id=product_id)[0].price
            product_name = Product.objects.filter(product_id=product_id)[0].product_name
            print(product_image)
            print(str(product_image))
            color = request.POST.get('color')
            size = request.POST.get('size')
            #creating or accesing the cart in or from sesssion
            cart = request.session.get('cart')
            if cart:
                exist = cart.get(product_id)
                if exist:
                    quantity = cart.get(product_id)[0]
                    cart[product_id][0] = quantity+1
                cart[product_id] = [1,2,3,4,5,6,7,8]
                cart[product_id][0] = 1
                cart[product_id][1] = size
                cart[product_id][2] = color
                cart[product_id][3] = str(product_image)
                cart[product_id][4] = int(str(product_price))
                cart[product_id][5] = str(product_name)
                cart[product_id][6] = str(product_id)

                print("new item " ,cart)
            else:
                cart = {}
                cart[product_id] = [1,2,3,4,5,6,7,8]
                cart[product_id][0] = 1
                cart[product_id][1] = size
                cart[product_id][2] = color
                cart[product_id][3] = str(product_image)
                cart[product_id][4] = int(str(product_price))
                cart[product_id][5] = str(product_name)
                cart[product_id][6] = str(product_id)
            request.session['cart'] = cart
            qty = cart[product_id][0]
            
            print(request.session['cart'])

            print(size)
            print(color)
            print(product_id)
            return render(request, 'quick-view.html', {'product':product[0],'colors':colors,'sizes':sizes,'cart_item':cart_item,'qty':qty,'comments':comments})
        
        elif oper == "1":
            product_id = request.POST.get('product')
            cart = request.session.get('cart')
            quantity = cart.get(product_id)[0]
            print(quantity)
            cart[product_id][0] = quantity+1
            qty = cart[product_id][0]
            print(qty)
            request.session['cart'] = cart
            
            print(request.session['cart'])
            return render(request, 'quick-view.html', {'product':product[0],'colors':colors,'sizes':sizes,'cart_item':cart_item,'qty':qty,'comments':comments})
        
        elif oper == "0":
            product_id = request.POST.get('product')
            cart = request.session.get('cart')
            quantity = cart.get(product_id)[0]
            print(quantity)
            cart[product_id][0] = quantity-1
            request.session['cart'] = cart
            qty = cart[product_id][0]
            if int(cart[product_id][0]) == 0:
                cart_item = False
                cart.pop(product_id)
                qty=0
            request.session['cart'] = cart
            print(request.session['cart'])
            oper = 3
            return render(request, 'quick-view.html', {'product':product[0],'colors':colors,'sizes':sizes,'cart_item':cart_item,'qty':qty,'comments':comments})



    # a simple filter
    qty = 0
    #for key in list(request.session.keys()):
     #   del request.session[key]
    cart = request.session.get('cart')  
    cart_item = False
    if cart:
        for key in cart.keys():
            if int(key) == my_id:
                qty = cart[key][0]
                cart_item = True
            
    print(cart_item)
    print(colors)
    print(sizes)
    
    return render(request, 'quick-view.html', {'product':product[0],'colors':colors,'sizes':sizes,'cart_item':cart_item,'qty':qty,'comments':comments})



def postComment(request):
    if request.method == "POST":
        comment=request.POST.get('message')
        user=request.user
        proId =request.POST.get('proId')
        product= Product.objects.get(product_id=proId)
        comment=ProductComment(comment= comment, user=user, product=product)
        comment.save()
        messages.success(request, "Your comment has been posted successfully")
        
    return redirect(f"/product/{proId}")







@login_required(login_url='/login')
def ViewCart(request):
    cart = request.session.get('cart')
    if cart:
        return render(request,'cart.html')
    return HttpResponse('no item in cart')


def Clear_cart(request):
    del request.session['cart']
    return redirect('home')

@login_required(login_url='/login')
def Profile(request):
    user = request.user
    orders = Orders.objects.filter(user=user)
    all_orders = []
    if orders:
        for order in orders:
            order.items_json = ast.literal_eval(order.items_json)
            print(type(order.items_json))
            all_orders.append(order)
    print(all_orders)
    all_orders = all_orders[::-1]
    for i in all_orders:
            print(i.items_json)
            print(type(i.items_json))
    return render(request,'profile.html',{'all_orders':all_orders})


@login_required(login_url='/login')
def Checkout(request):
    cart = request.session.get('cart')
    if request.method == "POST":
        name=request.POST.get('name')
        phone=request.POST.get('phone')
        landmark=request.POST.get('landmark')
        city=request.POST.get('city')
        zip=request.POST.get('zip')
        user = request.user
        amount=request.POST.get('amount')
        print(amount)
        print('--------------------------------------------------')
        order = Orders(items_json=str(cart), name=name, address=landmark, city=city,
                        zip_code=zip, phone=phone, amount=int(amount),user=user)
        order.save(force_insert=True)
        if request.session['cart']:
            del request.session['cart']
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        
        return HttpResponse("This project is not in Production so, I deactivated the payment getway. For Order Confirmation you can visit your profile. Thanks!!")
        
        thank = True
        id = order.order_id
        # return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
        # Request paytm to transfer the amount to your account after payment by user
        param_dict = {

                'MID': 'Your-Merchant-Id-Here',
                'ORDER_ID': str(order.order_id),
                'TXN_AMOUNT': str(amount),
                'CUST_ID': user.email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'shop/paytm.html', {'param_dict': param_dict})

    return render(request, 'shop/checkout.html')


@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})
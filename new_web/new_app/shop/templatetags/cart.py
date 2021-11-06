from django import template

register = template.Library()

@register.filter(name="is_in_cart")
def is_in_cart(product,cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return True
    return False

@register.filter(name="total")
def total(cart):
    total = 0
    print(len(cart))
    keys = cart.keys()
    for id in keys:
        price = int(cart[id][4])
        qty = int(cart[id][0])
        total_for_one = qty * price
        total = total+total_for_one 
    return total

@register.filter(name="count")
def count(cart):
    return len(cart)
    
@register.filter(name = 'cart_quantity')
def cart_quantity(product,cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.product_id:
            return cart.get(id)
    return 0

@register.filter(name = 'multiply')
def multiply(x,y):
    out = int(x) * int(y)
    return out

@register.filter(name = 'plus')
def plus(price):
    price = int(price)
    pta = price*46/100
    price = price+pta
    return int(price)

from shop.models import OrderUpdate
@register.filter(name = 'order_update')
def order_update(order_id):
    ou = OrderUpdate.objects.filter(order_id = order_id)[0]
    desc = ou.update_desc
    time = ou.timestamp
    return desc
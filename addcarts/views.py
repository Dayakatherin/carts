from django.shortcuts import render,response
from .models import Course,Cart
# Create your views here.

def cart_session(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart
def cart(request):
        if request.user.is_authenticated:
            cartitem = Cart.objects.filter(user=request.user,is_active=True)
        else:
            cart = Cart.objects.get(cart_id=cart_session(request))
            cartitem = Cart.objects.filter(cart=cart,is_active=True)
        count=cartitem.count()
        contxt = {
            'cartitem':cartitem,
            'count':count
        }
        return response(contxt)
def add_to_cart(request,course):
    user = request.user
    items = Course.objects.get(id=course)
    if user.is_authenticated:
       if Cart.objects.filter(course=items,user=user):
            cartitems = Cart.objects.get(course=items,user=user)
            cartitems.quantity +1
            cartitems.save()

       else:
            cartitems = Cart.objects.create(
              items = items,
              quantity = 1,
              user = user ,
            )
            cartitems.save()
    else:
        try:
            cart=Cart.objects.get(cart_id=cart_session(request))
        except:
            cart = Cart.objects.create(cart_id = cart_session(request)
            )
        cart.save()     
        try:
            cartitems = Cart.objects.get(items=items,cart=cart)
            cartitems.quantity +1
            cartitems.save()
        except:
           cartitems = Cart.objects.create(
              items = items,
              quantity = 1,
              cart = cart,
             )
        cartitems.save()

        


    


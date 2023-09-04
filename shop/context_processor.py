from .models import Product,Contact, Order, OrderUpdate, Cartrecord


def load_cart(request):
    params={}
    if request.user.is_authenticated:
        try:
            # fetching the cart details of the user
            param_cart=Cartrecord.objects.get(cart_user=request.user)
        except:
            object_cart=Cartrecord(cart_user=request.user)
            object_cart.save()
            param_cart=object_cart
        # passing the object containing the details of cart along with its its length 
        params['cart']=param_cart
        # params['cart_length']=len(param_cart.json_data)
    return params
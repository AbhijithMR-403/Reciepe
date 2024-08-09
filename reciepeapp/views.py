from django.http import HttpResponse, HttpResponseBadRequest
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
import razorpay
from .models import Recipe, CartItem, Order, ShoppingCart, OrderedProduct, Payment
from .forms import RecipeForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Sum, F


# Create your views here.


def home(request):
    return render(request, 'home.html')


def categories(request):
    return render(request, 'categories.html')


def blog(request):
    return render(request, 'blog.html')


def register(request):
    return render(request, 'signup.html')


def recipe(request):
    return render(request, 'recipe.html')


def contact(request):
    return render(request, 'contact.html')


def reviews(request):
    return render(request, 'reviews.html')


def login(request):
    return render(request, 'login.html')


def viewrecipe(request):
    return render(request, 'upload.html')


def hotel(request):
    return render(request, 'hotel.html')


def addtocart(request):
    return render(request, 'addtocart.html')


def sellrecipe(request):
    user = request.user
    dict_sell = {
        'sell': Recipe.objects.filter(user__id=user.id)
    }
    return render(request, 'sellrecipe.html', dict_sell)


def recipe_upload(request):
    recipes = Recipe.objects.all()

    if request.method == 'POST':

        title = request.POST.get('title')
        image_file = request.FILES.get('image')
        description = request.POST.get('description')
        price = request.POST.get('price')
        user = request.user

        if title and image_file and description:
            try:
                recipe = Recipe(title=title, image=image_file,
                                description=description, price=price,
                                user=User.objects.get(id=user.id))
                recipe.save()
                messages.success(request, "recipe uploaded")
                return redirect('recipe_upload')
            except Exception as e:
                messages.error(request, e)
        else:
            messages.error(request, "Details are not valid")
    context = {
        'recipes': recipes,
    }
    return render(request, 'upload.html', context)


def viewrecipe(request):
    user = request.user
    recipes = Recipe.objects.exclude(user__id=user.id)
    context = {
        'recipes': recipes,
    }
    return render(request, 'recipe.html', context)


def delete(request, pk):
    instance = Recipe.objects.get(pk=pk)
    instance.delete()
    recipes = Recipe.objects.all()
    context = {
        'recipes': recipes,
    }
    return render(request, 'recipe.html', context)


def edit(request, pk):
    instance_to_be_edited = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        frm = RecipeForm(request.POST, instance=instance_to_be_edited)
        if frm.is_valid():
            frm.save()
            return redirect('/viewrecipe/')
    else:
        frm = RecipeForm(instance=instance_to_be_edited)
    return render(request, 'create.html', {'frm': frm})


def add_to_cart(request, product_id):
    if request.method == 'POST':  # Ensure this is a POST request
        product = get_object_or_404(Recipe, id=product_id)
        user = request.user
        if (OrderedProduct.objects.filter(user=request.user, product=product)):
            return JsonResponse({
                'status': 'info',
                'message': 'You have already brought this Recipe',
                'product_id': product_id,
            })
        # check if the user has a cart or create new one for that user
        shopping_cart, cart_created = ShoppingCart.objects.get_or_create(
            user=user)

        # ckeck if the product is in that cart if no  then add product to that cart of that user
        cart_item, item_created = CartItem.objects.get_or_create(
            product=product, shopping_cart=shopping_cart)

        # if the product is already in the cart then add its quantity by 1
        if not item_created:
            return JsonResponse({
                'status': 'info',
                'message': 'Product is already added',
                'product_id': product_id,
            })

        return JsonResponse({
            'status': 'success',
            'message': 'Product added to cart',
            'product_id': product_id,
        })
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid request method'
        }, status=400)


def remove_cart_item(request, item_id):
    if request.method == 'POST':  # Ensure this is a POST request
        cart_item = get_object_or_404(CartItem, id=item_id)
        shopping_cart = cart_item.shopping_cart
        cart_item.delete()

        # Calculate the new total amount
        cart_items = CartItem.objects.filter(shopping_cart=shopping_cart)
        total_amount = cart_items.aggregate(total_amount=Sum(F('product__price')))[
            'total_amount'] or 0

        return JsonResponse({
            'status': 'success',
            'total_amount': total_amount,
            'message': 'Item removed from cart',
        })
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid request method'
        }, status=400)


def view_shopping_cart(request):
    user = request.user
    shopping_cart, created = ShoppingCart.objects.get_or_create(user=user)

    # fetch cart details and Cart items
    cart_items = CartItem.objects.filter(shopping_cart=shopping_cart)

    for item in cart_items:
        item.total_amount = item.product.price

    # total_quantity = sum(item.quantity for item in cart_items)
    total_amount = sum(item.total_amount for item in cart_items)

    context = {
        'cart_items': cart_items,
        # 'total_quantity': total_quantity,
        'total_amount': total_amount,
    }

    return render(request, 'addtocart.html', context)


# def remove_cart_item(request, item_id):
#     item = get_object_or_404(CartItem, id=item_id)
#     item.delete()

#     return redirect('view_shopping_cart')


def search_view(request, results=None):
    search = request.GET.get('search')
    if search:
        results = Recipe.objects.filter(title__icontains=search)
    else:
        results = Recipe.objects.all()

    context = {
        'results': results,
        'search': search,
    }

    return render(request, 'searchbar.html', context)


razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


def checkout(request):
    # Get the cart items for the logged-in user
    cart_items = CartItem.objects.filter(shopping_cart__user=request.user)
    if not cart_items.exists():
        messages.info(request, 'Add Item to cart')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('view_shopping_cart')))

    # Calculate the total amount
    total_amount = sum(item.product.price for item in cart_items)
    # vat_amount = total_amount * 0.18
    # delivery_amount = 4.95
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=total_amount*100,
                                                       currency='INR',
                                                       payment_capture='0'))

    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = '/paymenthandler/'
    order, _ = Order.objects.get_or_create(
        order_id=razorpay_order_id,
        user=request.user,
        total_amount=total_amount,
        status='Pending'
    )

    # Create OrderedProduct entries
    for cart_item in cart_items:
        OrderedProduct.objects.create(
            order=order,
            product=cart_item.product,
            user=request.user
        )

    context = {
        'cart_items': cart_items,
        'total_amount': total_amount,
        # 'vat_amount': vat_amount,
        # 'delivery_amount': delivery_amount,
    }
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = total_amount
    context['currency'] = 'INR'
    context['callback_url'] = callback_url

    return render(request, 'checkout.html', context)


@csrf_exempt
def paymenthandler(request):

    # only accept POST request.
    if request.method == "POST":
        print('hey this is you ')
        try:

            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            order = Order.objects.get(
                user=request.user, order_id=razorpay_order_id)
            print(order.total_amount)
            if result is not None:
                amount = int(order.total_amount * 100)

                try:
                    cart_items = CartItem.objects.filter(
                        shopping_cart__user=request.user)
                    razorpay_client.payment.capture(payment_id, amount)
                    Payment.objects.create(
                        order=order,
                        user=request.user,
                        transaction_id=payment_id,
                        payment_status='Success',
                        amount=order.total_amount
                    )
                    cart_items.delete()
                    # render success page on successful caputre of payment
                    return render(request, 'paymentSuccess.html')
                except Exception as e:
                    print(e)
                    Payment.objects.create(
                        order=order,
                        user=request.user,
                        transaction_id=payment_id,
                        payment_status='Failed',
                        amount=order.total_amount
                    )
                    # if there is an error while capturing payment.
                    return render(request, 'paymentFailure.html')
            else:

                # if signature verification fails.
                return render(request, 'paymentFailure.html')
        except:

            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()

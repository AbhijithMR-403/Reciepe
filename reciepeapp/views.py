from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe, CartItem, Order, ShoppingCart
from .forms import RecipeForm
from django.contrib import messages
from django.contrib.auth.models import User


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


def base(request):
    return render(request, 'base.html')


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
    dict_sell = {
        'sell': Recipe.objects.filter(user=request.user)
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
    recipes = Recipe.objects.exclude()
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
    product = get_object_or_404(Recipe, id=product_id)
    user = request.user

    # check if the user has a cart or create new one for that user
    shopping_cart, cart_created = ShoppingCart.objects.get_or_create(user=user)

    # ckeck if the product is in that cart if no  then add product to that cart of that user
    cart_item, item_created = CartItem.objects.get_or_create(
        product=product, shopping_cart=shopping_cart)

    # if the product is already in the cart then add its quantity by 1
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('view_shopping_cart')


def view_shopping_cart(request):
    user = request.user
    shopping_cart, created = ShoppingCart.objects.get_or_create(user=user)

    # fetch cart details and Cart items
    cart_items = CartItem.objects.filter(shopping_cart=shopping_cart)

    for item in cart_items:
        item.total_amount = item.product.price * item.quantity

    total_quantity = sum(item.quantity for item in cart_items)
    total_amount = sum(item.total_amount for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_quantity': total_quantity,
        'total_amount': total_amount,
    }

    return render(request, 'addtocart.html', context)


def remove_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()

    return redirect('view_shopping_cart')


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


def buy_now(request, item_id):
    user = request.user
    cart_item = get_object_or_404(
        CartItem, id=item_id, shopping_cart__user=user)
    total_amount = cart_item.product.price * cart_item.quantity

    context = {
        'total_amount': total_amount,
        'cart_item': cart_item,
        'razorpay_api_key': settings.RAZORPAY_API_KEY,
        'user': user
    }

    return render(request, 'payment.html', context)


@csrf_exempt
def handle_payment(request):
    if request.method == 'POST':
        user = request.user
        product_name = request.POST.get('product_name')
        total_amount = request.POST.get('total_amount')
        payment_id = request.POST.get('payment_id')

        # Save the order
        order = Order.objects.create(
            user=user,
            product_name=product_name,
            total_amount=total_amount,
            payment_id=payment_id
        )

        return JsonResponse({'message': 'Payment successful', 'order_id': order.id})

    return JsonResponse({'message': 'Invalid request'}, status=400)


def checkout(request):
    return render(request, 'checkout.html')

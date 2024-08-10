from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    # upload recipe
    path('recipe/', views.recipe_upload, name='recipe_upload'),
    path('contact/', views.contact, name='contact'),
    # path('base/', views.base, name='base'),
    path('order/', views.orderList, name='orderList'),
    path('viewrecipe/', views.viewrecipe, name='viewrecipe'),
    path('delete/<pk>', views.delete, name='delete'),
    path('edit/<pk>', views.edit, name='edit'),
    path('search/', views.search_view, name='search'),
    path('sellrecipe/', views.sellrecipe, name='sellrecipe'),
    path('addtocart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    # path('remove_cart_item/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('view_shopping_cart/', views.view_shopping_cart,
         name='view_shopping_cart'),
    path('remove_cart_item/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),

    # rahul added url
    path('recipeDetail/<int:id>', views.recipe_detail, name='recipe_detail_page'),

]

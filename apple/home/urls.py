from django.urls import path,include
from .views import HomeBaseView, ItemDetailView, register, Search, contact, add_to_cart,OrderSummeryView

app_name = 'home'
urlpatterns = [

    path('', HomeBaseView.as_view(),name = 'home'),
    path('product/<slug>',ItemDetailView.as_view(),name='product'),
    path('signup/',register,name = 'signup'),
    path('search/',Search.as_view(),name = 'search'),
    path('contact/',contact,name='contact'),
    path('cart/',OrderSummeryView.as_view(),name='cart'),
    path('add-to-cart/<slug>',add_to_cart,name='add-to-cart'),

    #
    # path('login/',login, name='product'),

]
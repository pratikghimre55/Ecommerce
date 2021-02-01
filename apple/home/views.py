from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect,get_object_or_404

# Create your views here.

#def homeview(request):
#
#    return render(request,'shop-login.html')
from django.views.generic import DetailView
from django.views.generic.base import View
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import SearchFilter,OrderingFilter
from home.models import Item, Brand, Ad, Slider, Category, Contact, OrderItem, Order
from home.serializers import UserSerializer,ItemSerializer


class BaseNavView(View):
    template_context = {}

class HomeBaseView(BaseNavView):
    def get(self,request):
        self.template_context['categorys'] = Category.objects.all()
        self.template_context['brands'] = Brand.objects.all()
        self.template_context['indexsale'] = Item.objects.filter(status = 'sale')
        self.template_context['indexhot'] = Item.objects.filter(status = 'hot')
        self.template_context['indexnew'] = Item.objects.filter(status = 'new')
        self.template_context['indexdefault'] = Item.objects.filter(status = 'default')
        self.template_context['ads']= Ad.objects.all()
        self.template_context['sliders'] = Slider.objects.all()
        return render(self.request,'shop-index.html',self.template_context)


#
# def itemdetail(request):
#
#     return render(request,'shop-item.html'

class ItemDetailView(DetailView):
    model = Item
    template_name = 'shop-item.html'

#
# def login(request):
#     return redirect(request, 'accounts/login.html')

def register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword= request.POST['cpassword']

        if password == cpassword:
            if User.objects.filter(username = username).exists():
                messages.error(request,"This username is already taken")
                return redirect('home:signup')
            if User.objects.filter(email = email).exists():
                messages.error(request, "This email is already taken")
                return redirect('home:signup')
            else:
                user = User.objects.create_user(
                    first_name = first_name,
                    last_name = last_name,
                    username = username,
                    email =  email,
                    password = password
                )
                user.save()

                messages.success(request, "SignUp is Successfull")
                return redirect('/accounts/login')
        else:
            messages.error(request,"Password is not matching")
            return redirect('home:signup')
    else:
        return render(request,'signup.html')

class Search(BaseNavView):
    def get(self,request):
        query = request.GET.get('query')
        if not query:
            return redirect('/')
        else:
            self.template_context['search_item'] = Item.objects.filter(
                title__icontains = query
            )

        return render(request,'shop-search-result.html',self.template_context)
def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        phone_no = request.POST['phone_no']
        address = request.POST['address']
        message = request.POST['message']
        email_address = request.POST['email_address']

        contact = Contact.objects.create(
            name = name,
            phone_no = phone_no,
            address = address,
            message = message,
            email_address = email_address
        )
        contact.save()
        messages.success(request, "Your message is sent successfully.")
        return redirect('home:contact')
    else:
        return render(request, 'contact.html')



# API part


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class ItemFilterListView(generics.ListAPIView):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()

    filter_backends = (DjangoFilterBackend,OrderingFilter,SearchFilter)
    filter_fields =['id','title','price','discounted_price']
    ordering_fields = ['id','price','title','discounted_price']
    search_fields = ['title','description']

def add_to_cart(request,slug):
    item = get_object_or_404(Item,slug=slug)
    order_item = OrderItem.objects.get_or_create(
        item = item,
        user = request.user,
        ordered = False

    )[0]
    orders = Order.objects.filter(
        user = request.user,
        ordered = False
    )
    if orders.exists():
        order = orders[0]
        if order.items.filter(item__slug = item.slug).exists():
            order_item.quantity +=1
            order_item.save()
            messages.success(request,"The Quantity is updated !")
            return redirect('/')
        else:
            order.items.add(order_item)
            messages.success(request, "The cart is added")
            return redirect('/')
    else:
        order = Order.objects.create(
            user = request.user
        )
        order.items.add(order_item)
        messages.success(request,"the cart is added")
        return redirect('/')

class OrderSummeryView(BaseNavView):
    #for dictionary we use kwargs
    def get(self,*args,**kwargs):
        try:
            order = Order.objects.get(
                user = self.request.user,
                ordered = False
            )
            self.template_context['object'] = order
        except:
            return redirect('/')

        return render(self.request,'shop-shopping-cart.html',self.template_context)
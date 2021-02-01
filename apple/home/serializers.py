from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

from home.models import Item


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password']

class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = ['id','title','price','discounted_price','image']
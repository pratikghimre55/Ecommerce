from rest_framework import routers
from django.urls import path, include
from home.views import UserViewSet,ItemViewSet,ItemFilterListView

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('Item', ItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('items',ItemFilterListView.as_view(),name= 'items'),
]
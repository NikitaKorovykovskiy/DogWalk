from django.urls import path, include
from dw.views import GetOrder
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"walk_orders", GetOrder, basename=r"walk_orders")

urlpatterns = [
    path("", include(router.urls), name="api"),
]
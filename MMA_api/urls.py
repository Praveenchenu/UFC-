from django.urls import path,include

from .views import Fighters_CRUD_api_View
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'fightersinfo', Fighters_CRUD_api_View)

urlpatterns = [
    path('', include(router.urls)),
]

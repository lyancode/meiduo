from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('areas', views.AreasViewSet, base_name='area')

urlpatterns = [
    # url('', include(router.urls))
]

urlpatterns += router.urls

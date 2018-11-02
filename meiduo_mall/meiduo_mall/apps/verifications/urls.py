from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'image_codes/(?P<image_code_id>\d+)/$', views.ImageCodeView.as_view())
]
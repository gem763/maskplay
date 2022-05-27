from django.urls import path
from django.conf.urls import include
from . import views as v

urlpatterns = [
    path('intro/', v.index, name='index'),
    path('', v.bbs, name='bbs'),
    path('test/', v.test, name='test'),
]

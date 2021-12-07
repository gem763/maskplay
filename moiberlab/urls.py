from django.urls import path
from django.conf.urls import include
from . import views as v

urlpatterns = [
    # path('mvp1', v.play, name='play'),
    path('', v.index, name='index'),
]

from django.urls import path
from django.conf.urls import include
from . import views as v

urlpatterns = [
    path('', v.play, name='play'),
    path('accounts/', include('allauth.urls')),
    path('my/', v.my, name='my'),
    path('user/<int:user_id>/boo/set/<int:boo_id>/', v.set_boo),
]

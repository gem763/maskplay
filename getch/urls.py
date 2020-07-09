from django.urls import path
from django.conf.urls import include
from . import views as v

urlpatterns = [
    path('', v.play, name='play'),
    path('accounts/', include('allauth.urls')),
    path('mypage/', v.mypage, name='mypage'),
    path('profiler/', v.profiler, name='profiler'),
    path('boochooser/', v.boochooser, name='boochooser'),
    path('user/<int:user_id>/boo/set/<int:boo_id>/', v.set_boo),
    # path('test/<str:state>/', v.test)
]

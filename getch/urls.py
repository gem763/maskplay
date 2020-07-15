from django.urls import path
from django.conf.urls import include
from . import views as v

urlpatterns = [
    path('', v.play, name='play'),
    path('accounts/', include('allauth.urls')),
    path('mypage/', v.mypage, name='mypage'),
    path('profiler/', v.profiler, name='profiler'),
    path('boochooser/', v.boochooser, name='boochooser'),
    path('slides/', v.slides, name='slides'),
    path('user/<int:user_id>/boo/set/<int:boo_id>/', v.set_boo),
    path('post/<int:post_id>/vote/', v.vote, name='vote'),
    path('post/<int:post_id>/vote/cancel/', v.vote_cancel, name='vote_cancel'),
    # path('test/<str:state>/', v.test)
]

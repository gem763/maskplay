from django.urls import path
from django.conf.urls import include
from . import views as v

urlpatterns = [
    path('', v.play, name='play'),
    path('accounts/', include('allauth.urls')),
    # path('mypage/', v.mypage, name='mypage'),
    path('authorpage/<int:boo_id>/', v.authorpage, name='authorpage'),
    # path('profiler/', v.profiler, name='profiler'),
    # path('boochooser/', v.boochooser, name='boochooser'),
    # path('posts/', v.posts, name='posts'),
    # path('posting/', v.posting, name='posting'),
    # path('user/<int:user_id>/boo/set/<int:boo_id>/', v.set_boo),
    path('post/<int:post_id>/vote/', v.vote, name='vote'),
    # path('post/<int:post_id>/vote/cancel/', v.vote_cancel, name='vote_cancel'),
    path('post/save/', v.post_save, name='post_save'),
    path('post/<int:post_id>/delete/', v.post_delete, name='post_delete'),
    path('boo/<int:boo_id>/follow/', v.follow, name='follow'),
    path('boo/<int:boo_id>/unfollow/', v.unfollow, name='unfollow'),
    path('boo/<int:boo_id>/set/', v.set_boo, name='set_boo'),
    path('boo/<int:boo_id>/network/', v.network, name='network'),
    path('boo/<int:boo_id>/posts/', v.boo_posts, name='boo_posts'),
    path('boo/profile/save/', v.profile_save, name='profile_save'),
    path('boo/new/', v.boo_new, name='boo_new'),

    # path('cuser/', v.cuser, name='cuser'),
]

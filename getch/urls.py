from django.urls import path
from django.conf.urls import include
from . import views as v

urlpatterns = [
    path('', v.play, name='play'),
    path('privacy/', v.privacy, name='privacy'),
    path('policy/', v.policy, name='policy'),
    path('accounts/', include('allauth.urls')),
    # path('authorpage/<int:boo_id>/', v.authorpage, name='authorpage'),
    # path('posts/', v.get_posts, name='get_posts'),
    # path('posts/ids/', v.get_iposts, name='get_iposts'),
    path('posts/ids/', v.get_iposts, name='get_iposts'),
    path('post/<int:post_id>/', v.get_post, name='get_post'),
    path('post/<int:post_id>/boo/', v.get_boopost, name='get_boopost'),
    path('post/<int:post_id>/vote/', v.vote, name='vote'),
    path('post/<int:post_id>/voters/', v.voters, name='voters'),
    path('post/save/', v.post_save, name='post_save'),
    path('post/<int:post_id>/delete/', v.post_delete, name='post_delete'),
    path('comment/save/', v.comment_save, name='comment_save'),
    path('boo/<int:boo_id>/follow/', v.follow, name='follow'),
    path('boo/<int:boo_id>/unfollow/', v.unfollow, name='unfollow'),
    path('boo/<int:boo_id>/set/', v.set_boo, name='set_boo'),
    path('boo/<int:boo_id>/network/', v.network, name='network'),
    # path('boo/<int:boo_id>/posts/', v.boo_posts, name='boo_posts'),
    path('boo/<int:boo_id>/iposts/', v.get_ibooposts, name='get_ibooposts'),
    path('boo/<int:boo_id>/profile/pix/', v.boo_profilepix, name='boo_profilepix'),
    # path('boo/<int:boo_id>/moreinfo/', v.boo_moreinfo, name='boo_moreinfo'),
    path('boo/profile/save/', v.profile_save, name='profile_save'),
    path('boo/new/', v.boo_new, name='boo_new'),
    path('user/', v.get_user, name='get_user'),
    path('user/other_boos/', v.other_boos, name='other_boos'),

]

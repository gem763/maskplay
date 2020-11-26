from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.apps import apps
from django.conf import settings
from django.core import serializers
from django.db.models import F
from django.template.loader import render_to_string
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
import getch.models as m
# import getch.serializers as ser
# from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
import os
import json

# https://brownbears.tistory.com/259
# https://stackoverflow.com/questions/37270170/iterate-through-a-static-image-folder-in-django
# characters = os.listdir(os.path.join(settings.BASE_DIR, 'getch\static', "materials\imgs\characters"))
# eye_masks = os.listdir(os.path.join(settings.BASE_DIR, 'getch\static', "materials\imgs\masks\eyes"))
# charac_imgs = os.listdir(os.path.join(settings.STATIC_ROOT, "materials\imgs\characters"))

# imgs = {
#     'characters': m.Character.objects.all()[:5],
#     'eyemasks': m.MaskBase.objects.filter(type='EYE')[:5],
# }

characters = {ch.id:{'category':ch.category, 'pix':ch.pix.url} for ch in m.Character.objects.all()}
eyemasks = {mb.id:{'category':mb.category, 'pix':mb.pix.url} for mb in m.MaskBase.objects.filter(type='EYE')}
mouthmasks = {mb.id:{'category':mb.category, 'pix':mb.pix.url} for mb in m.MaskBase.objects.filter(type='MOUTH')}
# maskbases = {mb.id:{'type':mb.type, 'category':mb.category, 'pix':mb.pix.url} for mb in m.MaskBase.objects.all()}

styletags = {t.id:t.tag for t in m.Styletag.objects.all()}
fashiontems = {t.id:t.item for t in m.Fashiontem.objects.all()}

stats = {
    'total_nboos': m.Boo.objects.count(),
    'total_nposts': m.Post.objects.count(),
    'total_nfollowers': m.Flager.objects.filter(status=m.FOLLOW).count(),
}

anonyboo = m.Boo.objects.get(pk=m.BOO_DELETED)


def test(request):
    return render(request, 'getch/test.html')

def policy(request):
    return render(request, 'getch/policy.html')

def privacy(request):
    return render(request, 'getch/privacy.html')

def play(request):
    # _qs = m.Post.objects.all().select_subclasses().order_by('-created_at')[:]
    # _qs = m.PostSerializer.setup_eager_loading(_qs)
    # _posts = m.PostSerializer(_qs, many=True).data
    # ctx = {'posts': json.dumps(_posts), 'characters':characters, 'maskbases':maskbases, 'stats':stats}
    # ctx = {'characters':characters, 'maskbases':maskbases, 'stats':stats}
    # print(characters)
    # ctx = {'characters':characters, 'eyemasks':eyemasks, 'mouthmasks':mouthmasks, 'stats':stats}
    ctx = {'stats':stats, 'styletags':styletags, 'fashiontems':fashiontems, 'anonyboo':anonyboo.serialized}
    # print(styletags)
    return render(request, 'getch/play.html', ctx)


def get_user(request):
    if request.user.is_authenticated:
        return JsonResponse({'success':True, 'user':request.user.serialized}, safe=False)
    else:
        return JsonResponse({'success':False})


# def get_posts(request):
#     _qs = m.Post.objects.all().select_subclasses().order_by('created_at')[:3]
#     _qs = m.PostSerializer.setup_eager_loading(_qs)
#     _posts = m.PostSerializer(_qs, many=True).data
#     return JsonResponse({'success':True, 'posts':_posts}, safe=False)

# def get_iposts(request):
#     _iposts = m.Post.objects.all().order_by('-created_at').values_list('id', flat=True)
#     return JsonResponse({'success':True, 'idlist':list(_iposts)}, safe=False)


def get_iposts(request, type):
    if type == 'history':
        _iposts = m.Post.objects.all().order_by('-created_at').values_list('id', flat=True)

    elif type == 'hot':
        _iposts = m.Post.objects.annotate(ordering=F('nvotes_up') + F('nvotes_down')).order_by('-ordering').values_list('id', flat=True)

    return JsonResponse({'success':True, 'idlist':list(_iposts)}, safe=False)


def get_post(request, post_id):
    _post = m.Post.objects.get_subclass(pk=post_id)
    _post = m.PostSerializer(_post).data
    return JsonResponse({'success':True, 'content':_post}, safe=False)


def get_ibooposts(request, boo_id):
    _boo = m.Boo.objects.get(pk=boo_id)
    return JsonResponse({'success':True, 'idlist':_boo.iposts}, safe=False)


def get_boopost(request, post_id):
    _post = m.Post.objects.get_subclass(pk=post_id)
    _post = m.BoopostSerializer(_post).data
    return JsonResponse({'success':True, 'content':_post}, safe=False)


def get_icomments(request, post_id):
    _icomments = m.Comment.objects.filter(post_id=post_id, boo__isnull=False).values_list('id', flat=True)
    return JsonResponse({'success':True, 'idlist':list(_icomments)}, safe=False)


def get_comment(request, comment_id):
    _comment = m.Comment.objects.get(pk=comment_id)
    _comment = m.CommentSerializer(_comment).data
    return JsonResponse({'success':True, 'content':_comment}, safe=False)


def get_ivoters(request, post_id, act):
    _ivoters = m.Flager.objects.filter(object_id=post_id, status=act).values_list('user_id', flat=True)
    return JsonResponse({'success':True, 'idlist':list(_ivoters)}, safe=False)

def get_voter(request, boo_id):
    _voter = m.Boo.objects.get(pk=boo_id)
    _voter = m.BasebooSerializer(_voter).data
    return JsonResponse({'success':True, 'content':_voter}, safe=False)

# def get_comments(request, post_id):
#     _comments = m.Comment.objects.filter(post_id=post_id)
#     _comments = m.CommentSerializer(_comments, many=True).data
#     return JsonResponse({'success':True, 'comments':_comments}, safe=False)


def other_boos(request):
    return JsonResponse({'success':True, 'other_boos':request.user.other_boos}, safe=False)


# def styletags_tag(request, tag_id):
#     try:
#         _tag = m.Styletag.objects.get(pk=tag_id)
#         request.user.boo.styletags.add(_tag)
#         return JsonResponse({'success':True, 'message':'styletag tagged successfully'}, safe=False)
#
#     except:
#         return JsonResponse({'success':False, 'message':'something wrong while tagging styletag'}, safe=False)
#
#
# def styletags_untag(request, tag_id):
#     try:
#         _tag = m.Styletag.objects.get(pk=tag_id)
#         request.user.boo.styletags.remove(_tag)
#         return JsonResponse({'success':True, 'message':'styletag untagged successfully'}, safe=False)
#
#     except:
#         return JsonResponse({'success':False, 'message':'something wrong while untagging styletag'}, safe=False)
#
#
# def fashiontems_tag(request, item_id):
#     try:
#         _item = m.Fashiontem.objects.get(pk=item_id)
#         request.user.boo.fashiontems.add(_item)
#         return JsonResponse({'success':True, 'message':'fashiontems tagged successfully'}, safe=False)
#
#     except:
#         return JsonResponse({'success':False, 'message':'something wrong while tagging fashiontem'}, safe=False)
#
#
# def fashiontems_untag(request, item_id):
#     try:
#         _item = m.Fashiontem.objects.get(pk=item_id)
#         request.user.boo.fashiontems.remove(_item)
#         return JsonResponse({'success':True, 'message':'fashiontem untagged successfully'}, safe=False)
#
#     except:
#         return JsonResponse({'success':False, 'message':'something wrong while untagging fashiontem'}, safe=False)


def boo_update(request):
    if request.method=='POST':
        print(request.POST, request.FILES)

        _styletags_to_add = request.POST.get('styletags_to_add', None)
        _styletags_to_remove = request.POST.get('styletags_to_remove', None)
        _fashiontems_to_add = request.POST.get('fashiontems_to_add', None)
        _fashiontems_to_remove = request.POST.get('fashiontems_to_remove', None)
        _boo_text = request.POST.get('boo_text', None)
        _boo_nick = request.POST.get('boo_nick', None)
        _profilepix = request.FILES.get('profilepix', None)

        try:
            if _styletags_to_add:
                request.user.boo.styletags.add(*json.loads(_styletags_to_add))

            if _styletags_to_remove:
                request.user.boo.styletags.remove(*json.loads(_styletags_to_remove))

            if _fashiontems_to_add:
                request.user.boo.fashiontems.add(*json.loads(_fashiontems_to_add))

            if _fashiontems_to_remove:
                request.user.boo.fashiontems.remove(*json.loads(_fashiontems_to_remove))

            if _boo_text:
                boo = request.user.boo
                boo.text = _boo_text
                boo.save()

            if _boo_nick:
                boo = request.user.boo
                boo.nick = _boo_nick
                boo.save()

            if _profilepix:
                profile = request.user.boo.profile
                profile.pix = _profilepix
                profile.save()

            return JsonResponse({'success':True, 'message':'boo updated successfully'}, safe=False)

        except:
            return JsonResponse({'success':False, 'message':'something wrong while boo updating'}, safe=False)


def boo_create(request):
    if request.method=='POST':
        print(request.POST, request.FILES)

        _styletags_to_add = request.POST.get('styletags_to_add', None)
        _styletags_to_remove = request.POST.get('styletags_to_remove', None)
        _fashiontems_to_add = request.POST.get('fashiontems_to_add', None)
        _fashiontems_to_remove = request.POST.get('fashiontems_to_remove', None)
        _boo_text = request.POST.get('boo_text', None)
        _boo_nick = request.POST.get('boo_nick', None)
        _profilepix = request.FILES.get('profilepix', None)

        boo = m.Boo.objects.create(user=request.user)

        try:
            if _styletags_to_add:
                boo.styletags.add(*json.loads(_styletags_to_add))

            if _styletags_to_remove:
                boo.styletags.remove(*json.loads(_styletags_to_remove))

            if _fashiontems_to_add:
                boo.fashiontems.add(*json.loads(_fashiontems_to_add))

            if _fashiontems_to_remove:
                boo.fashiontems.remove(*json.loads(_fashiontems_to_remove))

            if _boo_text:
                boo.text = _boo_text
                boo.save()

            if _boo_nick:
                boo.nick = _boo_nick
                boo.save()

            if _profilepix:
                profile = boo.profile
                profile.pix = _profilepix
                profile.save()


            request.user.set_boo(boo.id) # 새로 생성한 부캐를 선택하는 것이 디폴트
            return JsonResponse({'success':True, 'boo_id':boo.id, 'message':'boo created successfully'}, safe=False)

        except:
            return JsonResponse({'success':False, 'message':'something wrong while boo creating'}, safe=False)


def vote(request, post_id):
    action = request.GET.get('action', None)

    if action:
        post = m.Post.objects.get(pk=post_id)
        post.vote(int(action))
        return JsonResponse({'success':True, 'action':action}, safe=False)

    else:
        return JsonResponse({'success':False}, safe=False)


# def authorpage(request, boo_id):
#     boo = m.Boo.objects.get(pk=boo_id)
#     return render(request, 'getch/authorpage.html', {'author':boo})


def set_boo(request, boo_id):
    try:
        request.user.set_boo(boo_id)
        return JsonResponse({'success':True}, safe=False)
        # return JsonResponse({'success':True, 'voting_record':request.user.boo.voting_record}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


def follow(request, boo_id):
    try:
        request.user.boo.follow(boo_id)
        return JsonResponse({'success':True}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


def unfollow(request, boo_id):
    try:
        request.user.boo.unfollow(boo_id)
        return JsonResponse({'success':True}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


# def boo_posts(request, boo_id):
#     _posts = m.Post.objects.filter(boo_id=boo_id).select_subclasses().order_by('-created_at')
#     _posts = m.PostSerializer(_posts, many=True).data
#     return JsonResponse({'success':True, 'posts':json.dumps(_posts)}, safe=False)


def boo_profilepix(request, boo_id):
    _boo = m.Boo.objects.get(pk=boo_id)
    return JsonResponse({'success':True, 'pix':_boo.profile.pix.url}, safe=False)
    # return Response(_boo.data)


# def baseboo(request, boo_id):
#     _boo = m.Boo.objects.get(pk=boo_id)
#     _boo = m.BasebooSerializer(_boo).data
#     # print(_boo.data)
#     return JsonResponse({'success':True, 'boo':_boo}, safe=False)

# def boo_moreinfo(request, boo_id):
#     _boo = m.Boo.objects.get(pk=boo_id)
#     boo = { 'iposts': _boo.iposts }
#     return JsonResponse({'success':True, 'boo':boo}, safe=False)


def post_delete(request, post_id):
    try:
        post = m.Post.objects.get_subclass(pk=post_id)
        post.delete()
        return JsonResponse({'success':True, 'message':'post deleted successfully'}, safe=False)

    except:
        return JsonResponse({'success':False, 'message':'something wrong while deleting post'}, safe=False)


def voters(request, post_id):
    try:
        post = m.Post.objects.get(pk=post_id)
        return JsonResponse({'success':True, 'voters':post.voters}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


def profile_delete(request):
    try:
        request.user.delete_boo()
        return JsonResponse({'success':True, 'message':'boo deleted successfully'}, safe=False)

    except:
        return JsonResponse({'success':False, 'message':'something wrong while deleting boo'}, safe=False)


def profile_save(request):
    if request.method=='POST':
        print(request.POST, request.FILES)
        _nick = request.POST.get('nick', None)
        _text = request.POST.get('text', None)
        _key = request.POST.get('key', None)
        _profile_type = request.POST.get('profile_type', None)
        _profile_pix = request.FILES.get('profile_pix', None)
        _profile_image = request.FILES.get('profile_image_file', None)
        _profile_character = request.POST.get('profile_character', None)
        _profile_text = request.POST.get('profile_text', None)
        _profile_eyemask = request.POST.get('profile_eyemask', None)
        _profile_mouthmask = request.POST.get('profile_mouthmask', None)

        user = request.user
        boo_data = { 'profile': {} }

        if _nick:
            boo_data['nick'] = _nick

        if _text:
            boo_data['text'] = _text

        if _profile_type:
            boo_data['profile']['type'] = _profile_type

        if _profile_pix:
            boo_data['profile']['pix'] = _profile_pix

        if _profile_character:
            boo_data['profile']['character'] = _profile_character

        if _profile_image:
            boo_data['profile']['image'] = _profile_image

        if _profile_text:
            boo_data['profile']['text'] = _profile_text

        if _profile_eyemask:
            boo_data['profile']['eyemask'] = json.loads(_profile_eyemask)

        if _profile_mouthmask:
            boo_data['profile']['mouthmask'] = json.loads(_profile_mouthmask)

        if _key:
            boo_data['key'] = _key
            boo = m.Boo.objects.create(user=user)
            user.set_boo(boo.id) # 새로 생성한 부캐를 선택하는 것이 디폴트
            ser = m.BooSerializer(boo, data=boo_data)

        else:
            ser = m.BooSerializer(user.boo, data=boo_data)


        if ser.is_valid():
            boo = ser.save()
            return JsonResponse({'success':True, 'boo_id':boo.id, 'message':'boo saved successfully'}, safe=False)
            # return JsonResponse({'success':True, 'boo':boo.serialized}, safe=False)

        else:
            return JsonResponse({'success':False, 'message':'something wrong while saving boo'}, safe=False)



# def post_save(request):
#     if request.method=='POST':
#         print(request.POST, request.FILES)
#
#         post_id = request.POST.get('post_id', None)
#         post_type = request.POST.get('type', None)
#         text = request.POST.get('text', None)
#         pix = request.FILES.get('pix', None)
#         pix_a = request.FILES.get('pix_a', None)
#         pix_b = request.FILES.get('pix_b', None)
#
#         data = { 'boo': request.user.boo.id }
#
#         if text:
#             data['text'] = text
#
#         if pix:
#             data['pix'] = pix
#
#         if pix_a:
#             data['pix_a'] = pix_a
#
#         if pix_b:
#             data['pix_b'] = pix_b
#
#         if post_id:
#             mode = 'edited'
#             post = m.Post.objects.get_subclass(pk=post_id)
#             ser = m.PostSerializer(post, data=data, partial=True)
#
#         else:
#             mode = 'created'
#             data['type'] = post_type
#             ser = m.PostSerializer(data=data, partial=True)
#
#         ser.is_valid()
#         post_saved = ser.save()
#
#         print(post_saved.validated_data)
#
#         if mode == 'edited':
#             js = {'success':True, 'mode':mode}
#
#         elif mode == 'created':
#             js = {'success':True, 'mode':mode, 'post':post_saved.validated_data}
#             # post_created = render_to_string('getch/post.html', {'post':post, 'type':post_type})
#             # js = {'success':True, 'mode':mode, 'post_id':post.id, 'post_created':post_created}
#
#         return JsonResponse(js, safe=False)


def comment_save(request):
    if request.method == 'POST':
        print(request.POST)
        post_id = request.POST.get('post_id', None)
        text = request.POST.get('text', None)
        id = request.POST.get('id', None)

        if text and post_id:
            if id:
                comment = m.Comment.objects.get(pk=id)
                comment.text = text
                comment.save()

            else:
                comment = m.Comment.objects.create(boo=request.user.boo, post_id=post_id, text=text)

            return JsonResponse({'success':True, 'message':'successfully commented', 'comment_id':comment.id}, safe=False)

        else:
            return JsonResponse({'success':False, 'message':'something wrong on commenting'}, safe=False)



def post_save(request):
    if request.method == 'POST':
        print(request.POST, request.FILES)

        post_id = request.POST.get('post_id', None)
        post_type = request.POST.get('type', None)
        text = request.POST.get('text', None)
        keys = request.POST.get('keys', None)
        pix = request.FILES.get('pix', None)
        pix_a = request.FILES.get('pix_a', None)
        pix_b = request.FILES.get('pix_b', None)
        pixlabel_a = request.POST.get('pixlabel_a', None)
        pixlabel_b = request.POST.get('pixlabel_b', None)

        if post_id:
            mode = 'edited'
            post = m.Post.objects.get_subclass(pk=post_id)

        else:
            mode = 'created'
            postmodel = apps.get_model(app_label='getch', model_name=post_type)
            post = postmodel(boo=request.user.boo)

        if text:        post.text = text
        if keys:        post.keys = keys
        if pix:         post.pix = pix
        if pix_a:       post.pix_a = pix_a
        if pix_b:       post.pix_b = pix_b
        if pixlabel_a:  post.pixlabel_a = pixlabel_a
        if pixlabel_b:  post.pixlabel_b = pixlabel_b
        post.save()

        if mode == 'edited':
            js = {'success':True, 'mode':mode}

        elif mode == 'created':
            # _post = m.PostSerializer(post).data
            js = {'success':True, 'mode':mode, 'post_id':post.id}
            # js = {'success':True, 'mode':mode, 'post':_post}
            # post_created = render_to_string('getch/post.html', {'post':post, 'type':post_type})
            # js = {'success':True, 'mode':mode, 'post_id':post.id, 'post_created':post_created}

        return JsonResponse(js, safe=False)


def network(request, boo_id):
    boo = m.Boo.objects.get(pk=boo_id)
    return JsonResponse({'success':True, 'network':boo.network}, safe=False)


def boo_new(request):
    boo = m.Boo.objects.create(user=request.user)
    request.user.set_boo(boo.id) # 새로 생성한 부캐를 선택하는 것이 디폴트
    return JsonResponse({'success':True, 'boo':boo.serialized}, safe=False)


def search(request, keywords):
    n = 20
    # q = request.GET.get('q', None)

    try:
        vector = SearchVector('text', 'boo__nick', 'boo__text')
        query = SearchQuery(keywords)
        _searched = m.Post.objects.annotate(rank=SearchRank(vector, query)).order_by('-rank')[:n]
        print(_searched)
        _searched = _searched.values_list('id', flat=True)
        return JsonResponse({'success':True, 'idlist':list(_searched), 'message':'searched successfully'}, safe=False)

    except:
        return JsonResponse({'success':False, 'message':'something wrong while searching'}, safe=False)

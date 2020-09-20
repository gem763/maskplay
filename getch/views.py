from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.apps import apps
from django.conf import settings
from django.core import serializers
from django.template.loader import render_to_string
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

stats = {
    'total_nboos': m.Boo.objects.count(),
    'total_nposts': m.Post.objects.count(),
    'total_nfollowers': m.Flager.objects.filter(status=m.FOLLOW).count(),
}

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
    ctx = {'characters':characters, 'eyemasks':eyemasks, 'mouthmasks':mouthmasks, 'stats':stats}
    return render(request, 'getch/play.html', ctx)


def get_user(request):
    if request.user.is_authenticated:
        return JsonResponse({'success':True, 'user':request.user.serialized}, safe=False)
    else:
        return JsonResponse({'success':False})


def get_posts(request):
    _qs = m.Post.objects.all().select_subclasses().order_by('created_at')[:3]
    # _qs = m.Post.objects.all().select_subclasses().order_by('-created_at')[:3]
    _qs = m.PostSerializer.setup_eager_loading(_qs)
    _posts = m.PostSerializer(_qs, many=True).data
    return JsonResponse({'success':True, 'posts':_posts}, safe=False)
    # return JsonResponse({'success':True, 'posts':json.dumps(_posts)}, safe=False)


def get_post(request, post_id):
    _post = m.Post.objects.get_subclass(pk=post_id)
    _post = m.PostSerializer(_post).data
    return JsonResponse({'success':True, 'post':_post}, safe=False)


def get_basepost(request, post_id):
    _post = m.Post.objects.get_subclass(pk=post_id)
    _post = m.BasepostSerializer(_post).data
    return JsonResponse({'success':True, 'post':_post}, safe=False)


def other_boos(request):
    return JsonResponse({'success':True, 'other_boos':request.user.other_boos}, safe=False)


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


def boo_posts(request, boo_id):
    _posts = m.Post.objects.filter(boo_id=boo_id).select_subclasses().order_by('-created_at')
    _posts = m.PostSerializer(_posts, many=True).data
    return JsonResponse({'success':True, 'posts':json.dumps(_posts)}, safe=False)


def boo_profilepix(request, boo_id):
    _boo = m.Boo.objects.get(pk=boo_id)
    return JsonResponse({'success':True, 'pix':_boo.profile.pix.url}, safe=False)
    # return Response(_boo.data)


# def baseboo(request, boo_id):
#     _boo = m.Boo.objects.get(pk=boo_id)
#     _boo = m.BasebooSerializer(_boo).data
#     # print(_boo.data)
#     return JsonResponse({'success':True, 'boo':_boo}, safe=False)

def boo_moreinfo(request, boo_id):
    _boo = m.Boo.objects.get(pk=boo_id)
    boo = { 'iposts': _boo.iposts }
    return JsonResponse({'success':True, 'boo':boo}, safe=False)


def post_delete(request, post_id):
    try:
        post = m.Post.objects.get_subclass(pk=post_id)
        post.delete()
        return JsonResponse({'success':True}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


def voters(request, post_id):
    try:
        post = m.Post.objects.get(pk=post_id)
        return JsonResponse({'success':True, 'voters':post.voters}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


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
            return JsonResponse({'success':True, 'boo':boo.serialized}, safe=False)

        else:
            return JsonResponse({'success':False}, safe=False)



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
            _post = json.dumps(m.PostSerializer(post).data)
            js = {'success':True, 'mode':mode, 'post':_post}
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

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.apps import apps
from django.conf import settings
from django.core import serializers
from django.template.loader import render_to_string
import getch.models as m
# import getch.serializers as ser
# from rest_framework.renderers import JSONRenderer
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
    _qs = m.Post.objects.all().select_subclasses().order_by('-created_at')[:3]
    _qs = m.PostSerializer.setup_eager_loading(_qs)
    _posts = m.PostSerializer(_qs, many=True).data
    return JsonResponse({'success':True, 'posts':json.dumps(_posts)}, safe=False)


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


def authorpage(request, boo_id):
    boo = m.Boo.objects.get(pk=boo_id)
    return render(request, 'getch/authorpage.html', {'author':boo})


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


def post_delete(request, post_id):
    try:
        post = m.Post.objects.get_subclass(pk=post_id)
        post.delete()
        return JsonResponse({'success':True}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


def profile_save(request):
    if request.method=='POST':
        print(request.POST, request.FILES)
        _nick = request.POST.get('nick', None)
        _type = request.POST.get('type', None)
        _pix = request.FILES.get('pix', None)
        _image = request.FILES.get('image', None)
        _character = request.POST.get('character', None)
        _text = request.POST.get('text', None)
        _eyemask = request.POST.get('eyemask', None)
        _mouthmask = request.POST.get('mouthmask', None)

        user = request.user
        boo_data = { 'profile': {} }

        if _nick:
            boo_data['nick'] = _nick

        if _type:
            boo_data['profile']['type'] = _type

        if _pix:
            boo_data['profile']['pix'] = _pix

        if _character:
            boo_data['profile']['character'] = _character

        if _image:
            boo_data['profile']['image'] = _image

        if _text:
            boo_data['profile']['text'] = _text

        if _eyemask:
            boo_data['profile']['eyemask'] = json.loads(_eyemask)

        if _mouthmask:
            boo_data['profile']['mouthmask'] = json.loads(_mouthmask)

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

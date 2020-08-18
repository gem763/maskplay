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

imgs = {
    'characters': m.Character.objects.all(),
    'eyemasks': m.MaskBase.objects.filter(type='EYE'),
}

# characters = {}
# for ch in m.Character.objects.all():
#     if ch.category in characters:
#         characters[ch.category][ch.id] = ch.pix.url
#     else:
#         characters[ch.category] = { ch.id: ch.pix.url }
#
# maskbases = {}
# for mb in m.MaskBase.objects.all():
#     mb_type = mb.get_type_display()
#
#     if mb_type in maskbases:
#         if mb.category in maskbases[mb_type]:
#             maskbases[mb_type][mb.category][mb.id] = mb.pix.url
#         else:
#             maskbases[mb_type][mb.category] = { mb.id: mb.pix.url }
#
#     else:
#         maskbases[mb_type] = { mb.category: { mb.id: mb.pix.url } }


characters = {ch.id:{'category':ch.category, 'pix':ch.pix.url} for ch in m.Character.objects.all()}
maskbases = {mb.id:{'type':mb.type, 'category':mb.category, 'pix':mb.pix.url} for mb in m.MaskBase.objects.all()}


def play(request):
    posts = m.Post.objects.all().select_subclasses().order_by('-created_at')[:2]
    ctx = {'posts': posts, 'imgs':imgs, 'characters':characters, 'maskbases':maskbases}
    return render(request, 'getch/play.html', ctx)
    # return render(request, 'getch/test.html')


def vote(request, post_id):
    action = request.GET.get('action', None)

    if action:
        # boo_id = request.user.boo.pk
        post = m.Post.objects.get(pk=post_id)
        post.vote(int(action))
        # print(post.get_flags(status=0).count())

        # print('up vote: ', post.votes.user_ids(action=0))
        # print('down vote: ', post.votes.user_ids(action=1))
        # print('up voted: ', post.votes.exists(boo_id, action=0))
        # print('down voted: ', post.votes.exists(boo_id, action=1))
        # print(post.voters)
        # print(request.user.boo.voting_record)

        return JsonResponse({'success':True, 'action':action}, safe=False)

    else:
        return JsonResponse({'success':False}, safe=False)


def authorpage(request, boo_id):
    boo = m.Boo.objects.get(pk=boo_id)
    return render(request, 'getch/authorpage.html', {'author':boo})


def set_boo(request, boo_id):
    try:
        request.user.set_boo(boo_id)
        return JsonResponse({'success':True, 'voting_record':request.user.boo.voting_record}, safe=False)

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

        #
        # if _nick:
        #     boo.nick = _nick
        #
        # if _pix:
        #     boo.profile.pix = _pix
        #
        # if _pix_base:
        #     boo.profile.pix_base = _pix_base
        #
        # if _profile:
        #     boo.profile.type = _profile['type']
        #     boo.profile.txt = _profile['txt']
        #
        # boo.profile.save()
        # boo.save()
        # return JsonResponse({'success':True, 'profile':boo.profile.serialized, 'boo':boo.serialized}, safe=False)


def post_save(request):
    if request.method=='POST':
        post_id = request.POST.get('post_id', None)
        post_type = request.POST.get('type', None)
        text = request.POST.get('text', None)
        pix = request.FILES.get('pix', None)
        pix_a = request.FILES.get('pix_a', None)
        pix_b = request.FILES.get('pix_b', None)

        if post_id:
            post = m.Post.objects.get_subclass(pk=post_id)
            mode = 'edited'

        else:
            postmodel = apps.get_model(app_label='getch', model_name=post_type)
            post = postmodel()
            post.boo = request.user.boo
            mode = 'created'

        if text:    post.text = text
        if pix:     post.pix = pix
        if pix_a:   post.pix_a = pix_a
        if pix_b:   post.pix_b = pix_b
        post.save()

        print(request.POST, request.FILES)

        if mode == 'edited':
            js = {'success':True, 'mode':mode}

        elif mode == 'created':
            post_created = render_to_string('getch/post.html', {'post':post, 'type':post_type})
            js = {'success':True, 'mode':mode, 'post_id':post.id, 'post_created':post_created}

        return JsonResponse(js, safe=False)


def network(request, boo_id):
    boo = m.Boo.objects.get(pk=boo_id)
    return render(request, 'getch/network.html', {'boo':boo, 'open':1})


def boo_new(request):
    boo = m.Boo.objects.create(user=request.user)
    return JsonResponse({'success':True, 'boo':boo.serialized}, safe=False)

# def cuser(request):
#     # cuser = ser.UserSerializer([request.user], many=True).data[0]
#     # cuser = JSONRenderer().render(cuser)
#     try:
#         _cuser = ser.UserSerializer([request.user], many=True).data[0]
#         _cuser['boos'] = {boo.pop('id'):boo for boo in _cuser['boos']}
#         return JsonResponse({'success':True, 'cuser':_cuser}, safe=False)
#
#     except:
#         return JsonResponse({'success':False}, safe=False)

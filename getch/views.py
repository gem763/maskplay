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

# https://brownbears.tistory.com/259
# https://stackoverflow.com/questions/37270170/iterate-through-a-static-image-folder-in-django
characters = os.listdir(os.path.join(settings.BASE_DIR, 'getch\static', "materials\imgs\characters"))
eye_masks = os.listdir(os.path.join(settings.BASE_DIR, 'getch\static', "materials\imgs\masks\eyes"))
# charac_imgs = os.listdir(os.path.join(settings.STATIC_ROOT, "materials\imgs\characters"))

imgs = {
    'characters': characters,
    'eye_masks': m.MaskBase.objects.filter(type='EYE') #eye_masks,
}


def play(request):
    posts = m.Post.objects.all().select_subclasses().order_by('-created_at')
    ctx = {'posts': posts, 'imgs':imgs}
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
        pix = request.FILES.get('pix', None)

        profile = request.user.boo.profile
        profile.pix = pix
        profile.save()
        return JsonResponse({'success':True, 'pix_url':profile.pix.url}, safe=False)


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
            js = {'success':True, 'mode':mode, 'post_created':post_created}

        return JsonResponse(js, safe=False)


def network(request, boo_id):
    boo = m.Boo.objects.get(pk=boo_id)
    return render(request, 'getch/network.html', {'boo':boo, 'open':1})


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

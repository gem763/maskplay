from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.apps import apps
from django.conf import settings
from django.template.loader import render_to_string
import getch.models as m
import os

# https://brownbears.tistory.com/259
# https://stackoverflow.com/questions/37270170/iterate-through-a-static-image-folder-in-django
characters = os.listdir(os.path.join(settings.BASE_DIR, 'getch\static', "materials\imgs\characters"))
eye_masks = os.listdir(os.path.join(settings.BASE_DIR, 'getch\static', "materials\imgs\masks\eyes"))
# charac_imgs = os.listdir(os.path.join(settings.STATIC_ROOT, "materials\imgs\characters"))

imgs = {
    'characters': characters,
    'eye_masks': eye_masks,
}


def play(request):
    posts = m.Post.objects.all().select_subclasses().order_by('-created_at')
    ctx = {'posts': posts, 'imgs':imgs}
    return render(request, 'getch/play.html', ctx)


def posts(request):
    _posts = m.Post.objects.all().select_subclasses().order_by('-created_at')
    ctx = {'posts': _posts}
    return render(request, 'getch/posts.html', ctx)


def vote(request, post_id):
    action = request.GET.get('action', None)

    if action:
        boo_id = request.user.boo.pk
        post = m.Post.objects.get_subclass(pk=post_id)
        post.vote(int(action), boo_id)

        print('up vote: ', post.votes.user_ids(action=0))
        print('down vote: ', post.votes.user_ids(action=1))
        print('up voted: ', post.votes.exists(boo_id, action=0))
        print('down voted: ', post.votes.exists(boo_id, action=1))
        print('voted: ', post.voted(boo_id)) # post.voted 를 바꿨다... 이부분을 고쳐야함

        return JsonResponse({'success':True}, safe=False)

    else:
        return JsonResponse({'success':False}, safe=False)


def vote_cancel(request, post_id):
    pass
    # boo_id = request.user.boo.pk
    # post = m.Post.objects.get_subclass(pk=post_id)
    # post.vote(int(action), boo_id)


def mypage(request):
    return render(request, 'getch/mypage.html')


def profiler(request):
    ctx = {'imgs':imgs}
    return render(request, 'getch/profiler.html', ctx)


def boochooser(request):
    return render(request, 'getch/boochooser.html')


def set_boo(request, user_id, boo_id):
    user = m.User.objects.get(pk=user_id)
    # print(user)
    user.set_boo(boo_id)
    return JsonResponse({'success':True}, safe=False)


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

        else:
            postmodel = apps.get_model(app_label='getch', model_name=post_type)
            post = postmodel()
            post.boo = request.user.boo

        if text:    post.text = text
        if pix:     post.pix = pix
        if pix_a:   post.pix_a = pix_a
        if pix_b:   post.pix_b = pix_b
        post.save()

        print(request.POST, request.FILES)
        saved = render_to_string('getch/post.html', {'post':post, 'type':post_type})
        return JsonResponse({'success':True, 'saved':saved}, safe=False)

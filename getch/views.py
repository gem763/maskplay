from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import getch.models as m


def play(request):
    posts = m.Post.objects.all().select_subclasses()
    ctx = {'posts': posts}
    return render(request, 'getch/play.html', ctx)


def vote(request, post_id):
    action = request.GET.get('action', None)

    if action:
        post = m.Post.objects.get(pk=post_id)
        boo_id = request.user.boo().pk

        if action=='up':
            post.votes.up(boo_id)

        elif action=='down':
            post.votes.down(boo_id)

        return JsonResponse({'success':True}, safe=False)

    else:
        return JsonResponse({'success':False}, safe=False)


def mypage(request):
    return render(request, 'getch/mypage.html')


def profiler(request):
    return render(request, 'getch/profiler.html')


def boochooser(request):
    return render(request, 'getch/boochooser.html')


def set_boo(request, user_id, boo_id):
    user = m.User.objects.get(pk=user_id)
    # print(user)
    user.set_boo(boo_id)
    return JsonResponse({'success':True}, safe=False)

# def test(request, state):
#     print(state, '******************************')

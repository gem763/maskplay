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
        boo_id = request.user.boo().pk
        post = m.Post.objects.get(pk=post_id)
        post.vote(int(action), boo_id)

        print('up vote: ', post.votes.user_ids(action=0))
        print('down vote: ', post.votes.user_ids(action=1))
        # print(post.votes.all(boo_id, action=1), 'kkkkkkkkkkkkkkkk')

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

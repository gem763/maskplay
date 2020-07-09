from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import getch.models as m


def play(request):
    return render(request, 'getch/play.html')


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

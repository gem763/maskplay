from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import getch.models as m


def play(request):
    return render(request, 'getch/play.html')


def my(request):
    return render(request, 'getch/my_page.html')


def set_boo(request, user_id, boo_id):
    user = m.User.objects.get(pk=user_id)
    # print(user)
    user.set_boo(boo_id)
    return JsonResponse({'success':True}, safe=False)

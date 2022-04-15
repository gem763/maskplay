from django.shortcuts import render
from django.conf import settings

# Create your views here.

context = dict()

def index(request):
    request.session.save()
    # context['entry'] = request.GET.get('entry', None)
    # context['kakao_js_key'] = settings.KAKAO_JS_KEY
    return render(request, 'moiberlab/index.html', context)


def bbs(request):
    # request.session.save()
    # context['entry'] = request.GET.get('entry', None)
    # context['kakao_js_key'] = settings.KAKAO_JS_KEY
    return render(request, 'moiberlab/bbs.html', context)
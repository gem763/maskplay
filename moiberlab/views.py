from django.shortcuts import render
from django.conf import settings

# Create your views here.

context = dict()

def home(request):
    request.session.save()
    context['entry'] = request.GET.get('entry', None)
    context['kakao_js_key'] = settings.KAKAO_JS_KEY
    return render(request, 'moiberlab/home.html', context)

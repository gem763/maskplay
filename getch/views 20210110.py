from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.apps import apps
from django.conf import settings
from django.core import serializers
from django.db.models import F
from django.template.loader import render_to_string
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
import getch.models as m
# import getch.serializers as ser
# from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
import os
import json

styletags = {t.id:t.tag for t in m.Styletag.objects.all()}
fashiontems = {t.id:t.item for t in m.Fashiontem.objects.all()}

# labels = {
#     'gender': {l.id:{ 'key':l.key, 'label':l.label } for l in m.Genderlabel.objects.all()},
#     'age': {l.id:{ 'key':l.key, 'label':l.label } for l in m.Agelabel.objects.all()},
#     'body': {l.id:{ 'key':l.key, 'label':l.label } for l in m.Bodylabel.objects.all()},
#     'style': {l.id:{ 'key':l.key, 'label':l.label } for l in m.Stylelabel.objects.all()},
#     'item': {l.id:{ 'key':l.key, 'label':l.label } for l in m.Itemlabel.objects.all()}
# }

labels = {
    'gender': list(m.Genderlabel.objects.order_by('key').values('id', 'label')),
    'age': list(m.Agelabel.objects.order_by('key').values('id', 'label')),
    'body': list(m.Bodylabel.objects.order_by('key').values('id', 'label')),
    'style': list(m.Stylelabel.objects.order_by('key').values('id', 'label')),
    'item': list(m.Itemlabel.objects.order_by('key').values('id', 'label'))
}

stats = {
    'total_nboos': m.Boo.objects.count(),
    'total_nposts': m.Post.objects.count(),
    'total_nfollowers': m.Flager.objects.filter(status=m.FOLLOW).count(),
}

anonyboo = m.Boo.objects.get(pk=m.BOO_DELETED)


def test(request):
    return render(request, 'getch/test.html')

def policy(request):
    return render(request, 'getch/policy.html')

def privacy(request):
    return render(request, 'getch/privacy.html')

def recruit(request):
    return render(request, 'getch/recruit.html')

def play(request):
    ctx = {'stats':stats, 'labels':labels, 'styletags':styletags, 'fashiontems':fashiontems, 'anonyboo':anonyboo.serialized, 'req':0}
    return render(request, 'getch/play.html', ctx)

def company(request):
    ctx = {'stats':stats, 'styletags':styletags, 'fashiontems':fashiontems, 'anonyboo':anonyboo.serialized, 'req':1}
    return render(request, 'getch/play.html', ctx)

def company_recruit(request):
    ctx = {'stats':stats, 'styletags':styletags, 'fashiontems':fashiontems, 'anonyboo':anonyboo.serialized, 'req':2}
    return render(request, 'getch/play.html', ctx)

def landing(request):
    ctx = {'stats':stats, 'styletags':styletags, 'fashiontems':fashiontems, 'anonyboo':anonyboo.serialized, 'req':3}
    return render(request, 'getch/play.html', ctx)

# def profiler(request):
#     return JsonResponse({'test':'kkkkkkkkkkkkkkkkkkkkkk'}, safe=False)
#     # ctx = {'stats':stats, 'styletags':styletags, 'fashiontems':fashiontems, 'anonyboo':anonyboo.serialized, 'req':4}
#     # return render(request, 'getch/play.html', ctx)

def testbed(request):
    ctx = {'stats':stats, 'styletags':styletags, 'fashiontems':fashiontems, 'anonyboo':anonyboo.serialized, 'req':5}
    return render(request, 'getch/play.html', ctx)


def get_user(request):
    if request.user.is_authenticated:
        return JsonResponse({'success':True, 'user':request.user.serialized}, safe=False)
    else:
        return JsonResponse({'success':False})


def get_iposts(request, type):
    if type == 'history':
        _iposts = m.Post.objects.exclude(boo_id=m.BOO_DELETED).order_by('-created_at').values_list('id', flat=True)
        # _iposts = m.Post.objects.all().order_by('-created_at').values_list('id', flat=True)

    elif type == 'hot':
        _iposts = m.Post.objects.exclude(boo_id=m.BOO_DELETED).annotate(ordering=F('nvotes_up') + F('nvotes_down')).order_by('-ordering').values_list('id', flat=True)
        # _iposts = m.Post.objects.annotate(ordering=F('nvotes_up') + F('nvotes_down')).order_by('-ordering').values_list('id', flat=True)

    return JsonResponse({'success':True, 'idlist':list(_iposts)}, safe=False)


def get_post(request, post_id):
    try:
        _post = m.Post.objects.get_subclass(pk=post_id)
        _post = m.PostSerializer(_post).data
        return JsonResponse({'success':True, 'content':_post}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


def get_ibooposts(request, boo_id, type):
    try:
        _boo = m.Boo.objects.get(pk=boo_id)
        return JsonResponse({'success':True, 'idlist':_boo.iposts(type)}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


def get_boopost(request, post_id):
    try:
        _post = m.Post.objects.get_subclass(pk=post_id)
        # 내페이지에서 내가 작성하지 않은 포스트를 가져오는 경우가 있어서, PostSerializer로 바꿨다
        # 2020.12.07
        _post = m.PostSerializer(_post).data
        # _post = m.BoopostSerializer(_post).data
        return JsonResponse({'success':True, 'content':_post}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


def get_icomments(request, post_id):
    try:
        _icomments = m.Comment.objects.filter(post_id=post_id, boo__isnull=False).values_list('id', flat=True)
        return JsonResponse({'success':True, 'idlist':list(_icomments)}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


def get_comment(request, comment_id):
    try:
        _comment = m.Comment.objects.get(pk=comment_id)
        _comment = m.CommentSerializer(_comment).data
        return JsonResponse({'success':True, 'content':_comment}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


def get_ivoters(request, post_id, act):
    try:
        _ivoters = m.Flager.objects.filter(object_id=post_id, status=act).values_list('user_id', flat=True)
        return JsonResponse({'success':True, 'idlist':list(_ivoters)}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


def get_voter(request, boo_id):
    try:
        _voter = m.Boo.objects.get(pk=boo_id)
        _voter = m.BasebooSerializer(_voter).data
        return JsonResponse({'success':True, 'content':_voter}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


def other_boos(request):
    return JsonResponse({'success':True, 'other_boos':request.user.other_boos}, safe=False)


def _labels_add(target, what):
    target.add(*what)


def _labels_remove(target, what):
    target.remove(*what)


def _labels_update(boo, labels):
    # print(labels.items())

    for k, v in labels.items():
        for _k, _v in v.items():
            if _k=='add':
                getattr(boo, k).add(*_v)
            if _k=='remove':
                getattr(boo, k).remove(*_v)

def boo_update(request):
    if request.method=='POST':
        print(request.POST, request.FILES)
        # print(json.loads(request.POST.get('labels', None)))
        # return
        #
        # _styletags_to_add = request.POST.get('styletags_to_add', None)
        # _styletags_to_remove = request.POST.get('styletags_to_remove', None)
        # _fashiontems_to_add = request.POST.get('fashiontems_to_add', None)
        # _fashiontems_to_remove = request.POST.get('fashiontems_to_remove', None)
        _labels = request.POST.get('labels', None)
        _boo_text = request.POST.get('boo_text', None)
        _boo_nick = request.POST.get('boo_nick', None)
        _profilepix = request.FILES.get('profilepix', None)

        try:
            if _labels:
                # request.user.boo['genderlabels'].add(2)
                # print(request.user.boo.genderlabels)
                # return
                _labels_update(request.user.boo, json.loads(_labels))

            # if _styletags_to_add:
            #     request.user.boo.styletags.add(*json.loads(_styletags_to_add))
            #
            # if _styletags_to_remove:
            #     request.user.boo.styletags.remove(*json.loads(_styletags_to_remove))
            #
            # if _fashiontems_to_add:
            #     request.user.boo.fashiontems.add(*json.loads(_fashiontems_to_add))
            #
            # if _fashiontems_to_remove:
            #     request.user.boo.fashiontems.remove(*json.loads(_fashiontems_to_remove))

            if _boo_text:
                boo = request.user.boo
                boo.text = _boo_text
                boo.save()

            if _boo_nick:
                boo = request.user.boo
                boo.nick = _boo_nick
                boo.save()

            if _profilepix:
                profile = request.user.boo.profile
                profile.pix = _profilepix
                profile.save()

            return JsonResponse({'success':True, 'message':'boo updated successfully'}, safe=False)

        except:
            return JsonResponse({'success':False, 'message':'something wrong while boo updating'}, safe=False)


def boo_create(request):
    if request.method=='POST':
        print(request.POST, request.FILES)

        _styletags_to_add = request.POST.get('styletags_to_add', None)
        _styletags_to_remove = request.POST.get('styletags_to_remove', None)
        _fashiontems_to_add = request.POST.get('fashiontems_to_add', None)
        _fashiontems_to_remove = request.POST.get('fashiontems_to_remove', None)
        _boo_text = request.POST.get('boo_text', None)
        _boo_nick = request.POST.get('boo_nick', None)
        _profilepix = request.FILES.get('profilepix', None)

        boo = m.Boo.objects.create(user=request.user)

        try:
            if _styletags_to_add:
                boo.styletags.add(*json.loads(_styletags_to_add))

            if _styletags_to_remove:
                boo.styletags.remove(*json.loads(_styletags_to_remove))

            if _fashiontems_to_add:
                boo.fashiontems.add(*json.loads(_fashiontems_to_add))

            if _fashiontems_to_remove:
                boo.fashiontems.remove(*json.loads(_fashiontems_to_remove))

            if _boo_text:
                boo.text = _boo_text
                boo.save()

            if _boo_nick:
                boo.nick = _boo_nick
                boo.save()

            if _profilepix:
                profile = boo.profile
                profile.pix = _profilepix
                profile.save()


            request.user.set_boo(boo.id) # 새로 생성한 부캐를 선택하는 것이 디폴트
            return JsonResponse({'success':True, 'boo_id':boo.id, 'message':'boo created successfully'}, safe=False)

        except:
            return JsonResponse({'success':False, 'message':'something wrong while boo creating'}, safe=False)


def vote(request, post_id):
    action = request.GET.get('action', None)
    fit = request.user.boo.fit

    if action:
        post = m.Post.objects.get(pk=post_id)
        post.vote(int(action))
        return JsonResponse({'success':True, 'action':action, 'fit':fit}, safe=False)

    else:
        return JsonResponse({'success':False}, safe=False)



def set_boo(request, boo_id):
    try:
        request.user.set_boo(boo_id)
        return JsonResponse({'success':True}, safe=False)

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


def like_comment(request, comment_id):
    try:
        comment = m.Comment.objects.get(pk=comment_id)
        # print(comment)
        comment.like(request.user.boo)
        return JsonResponse({'success':True, 'message':'Comment liked successfully'}, safe=False)

    except:
        return JsonResponse({'success':False, 'message':'Something wrong when liking comment'}, safe=False)


def delike_comment(request, comment_id):
    try:
        comment = m.Comment.objects.get(pk=comment_id)
        comment.delike(request.user.boo)
        return JsonResponse({'success':True, 'message':'Comment deliked successfully'}, safe=False)

    except:
        return JsonResponse({'success':False, 'message':'Something wrong when deliking comment'}, safe=False)


def boo_profilepix(request, boo_id):
    _boo = m.Boo.objects.get(pk=boo_id)
    return JsonResponse({'success':True, 'pix':_boo.profile.pix.url}, safe=False)


def post_delete(request, post_id):
    try:
        post = m.Post.objects.get_subclass(pk=post_id)
        post.delete()
        return JsonResponse({'success':True, 'message':'post deleted successfully'}, safe=False)

    except:
        return JsonResponse({'success':False, 'message':'something wrong while deleting post'}, safe=False)


def voters(request, post_id):
    try:
        post = m.Post.objects.get(pk=post_id)
        return JsonResponse({'success':True, 'voters':post.voters}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


def profile_delete(request):
    try:
        request.user.delete_boo()
        return JsonResponse({'success':True, 'message':'boo deleted successfully'}, safe=False)

    except:
        return JsonResponse({'success':False, 'message':'something wrong while deleting boo'}, safe=False)



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
            # _post = m.PostSerializer(post).data
            js = {'success':True, 'mode':mode, 'post_id':post.id}
            # js = {'success':True, 'mode':mode, 'post':_post}
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


def search(request, keywords):
    n = 20
    # q = request.GET.get('q', None)

    try:
        vector = SearchVector('text', 'boo__nick', 'boo__text')
        query = SearchQuery(keywords)
        _searched = m.Post.objects.annotate(rank=SearchRank(vector, query)).order_by('-rank')[:n]
        print(_searched)
        _searched = _searched.values_list('id', flat=True)
        return JsonResponse({'success':True, 'idlist':list(_searched), 'message':'searched successfully'}, safe=False)

    except:
        return JsonResponse({'success':False, 'message':'something wrong while searching'}, safe=False)

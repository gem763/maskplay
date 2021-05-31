from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.apps import apps
from django.conf import settings
from django.core import serializers
# from django.db.models import F
# from django.db.models import Q
from django.db.models import F, Q, Sum, Count, Case, When
from django.template.loader import render_to_string
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramSimilarity
import getch.models as m
from allauth.account.views import LoginView, LogoutView
# import getch.serializers as ser
# from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from notifications.signals import notify
import random
import os
import json
from datetime import datetime, date, timedelta

labels = {
    'gender': list(m.Genderlabel.objects.order_by('key').values('id', 'label')),
    'age': list(m.Agelabel.objects.order_by('key').values('id', 'label')),
    'body': list(m.Bodylabel.objects.order_by('key').values('id', 'label')),
    'style': list(m.Stylelabel.objects.order_by('key').values('id', 'label')),
    'item': list(m.Itemlabel.objects.order_by('key').values('id', 'label'))
}

# stats = {
#     'total_nboos': m.Boo.objects.count(),
#     'total_nposts': m.Post.objects.count(),
#     'total_nfollowers': m.Flager.objects.filter(status=m.FOLLOW).count(),
# }

# anonyboo = m.Boo.objects.get(pk=m.BOO_DELETED)
context = { 'labels':labels }

def test(request):
    return render(request, 'getch/test.html')

def discover(request):
    request.session.save()
    context['entry'] = request.GET.get('entry', None)
    context['dongne'] = request.GET.get('dongne', None)
    context['gender'] = request.GET.get('gender', None)
    return render(request, 'getch/moiber/discover.html', context)


def policy(request):
    return render(request, 'getch/policy.html')

def privacy(request):
    return render(request, 'getch/privacy.html')

def recruit(request):
    return render(request, 'getch/recruit.html')

def load(request, ctx):
    # 처음 로딩할때는 session 객체가 없어서,
    # 이렇게 save()해주면 새로 생기면서 session_key가 만들어진다
    # 즉 로그인 안했을때도 session_key를 쓸수 있다
    # 이후 로그인하면 해당 session_key가 유지되도록 설정: setting에서 SESSION_ENGINE = 'getch.session_backend'
    # 로그아웃 하면, 해당 session이 지워지고, 이 부분의 코드가 다시 실행되면서 새로운 session_key가 생성된다
    # 2021.02.19
    request.session.save()

    if request.user.is_authenticated:
        if request.user.is_staff:
            ctx['utype'] = 'staff'
        else:
            ctx['utype'] = 'general'

    else:
        ctx['utype'] = 'guest'

    # print(m.Flager.objects.filter(status=0, user_id=59, object_id=0).values('user'))

    return render(request, 'getch/play.html', ctx)

def play(request):
    # hotboos_id = m.Flager.objects.filter(status=10).values('object_id').annotate(nfollowers=Count('object_id')).order_by('-nfollowers')[:5].values_list('id', flat=True)
    # notify.send(request.user, recipient=request.user, verb='you reached level 10')

    # _iboos = m.Flager.objects.filter(status=m.FOLLOW).values('object_id').annotate(nfollowers=Count('object_id')).order_by('-nfollowers')[:10].values_list('object_id', flat=True)

    # print(_flags)

    context['req'] = 0
    return load(request, context)


def company(request):
    context['req'] = 1
    return load(request, context)

def company_recruit(request):
    context['req'] = 2
    return load(request, context)

def landing(request):
    context['req'] = 3
    return load(request, context)

def testbed(request):
    context['req'] = 5
    return load(request, context)

def testfeed(request):
    context['req'] = 6
    return load(request, context)



def get_user(request):
    sessionkey = request.session.session_key

    if request.user.is_authenticated:
        if request.user.has_active_boo:
            return JsonResponse({'success':True, 'user':request.user.serialized, 'guestboo':m.Boo.guestboo_serialized(sessionkey)}, safe=False)
        else:
            request.user.create_default_boo()
            return JsonResponse({'success':True, 'user':request.user.serialized, 'first_visit':True, 'guestboo':m.Boo.guestboo_serialized(sessionkey)}, safe=False)

    else:
        return JsonResponse({'success':False, 'guestboo':m.Boo.guestboo_serialized(sessionkey)})


def get_user2(request):
    sessionkey = request.session.session_key

    if request.user.is_authenticated:
        if not request.user.has_active_boo:
            request.user.create_default_boo()

        return JsonResponse({'success':True, 'user':request.user.serialized2, 'guestboo':m.Boo.guestboo_serialized(sessionkey)}, safe=False)
        # return JsonResponse({'success':True, 'user':request.user.serialized2, 'first_visit':True, 'guestboo':m.Boo.guestboo_serialized(sessionkey)}, safe=False)

    else:
        return JsonResponse({'success':False, 'guestboo':m.Boo.guestboo_serialized(sessionkey)})


def get_ipixs(request):
    _ipixs = list(m.Pix.ipixs())
    random.shuffle(_ipixs)
    return JsonResponse({'success':True, 'ids':_ipixs}, safe=False)


def get_icols(request):
    _icols = m.Collection.icols()
    random.shuffle(_icols)
    return JsonResponse({'success':True, 'ids':_icols}, safe=False)


def get_pix(request, pix_id):
    try:
        _pix = m.Pix.objects.get(pk=pix_id)
        _pix = m.PixSerializer(_pix).data
        return JsonResponse({'success':True, 'content':_pix}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


def collect_pix(request, collection_id, pix_id):
    try:
        pick = m.Pick.objects.create(collection_id=collection_id, pix_id=pix_id)
        return JsonResponse({'success':True, 'pick_id':pick.id, 'message':'pix collected successfully'}, safe=False)

    except:
        return JsonResponse({'success':False, 'message':'something wrong while collecting pix'}, safe=False)


def get_ipicks(request, collection_id):
    _ipicks = m.Collection.objects.get(pk=collection_id).ipicks
    return JsonResponse({'success':True, 'ids':_ipicks}, safe=False)


def get_collection(request, collection_id):
    _col = m.Collection.objects.get(id=collection_id)
    return JsonResponse({'success':True, 'content':_col.serialized}, safe=False)


def get_collection_base(request, collection_id):
    _col = m.Collection.objects.get(id=collection_id)
    return JsonResponse({'success':True, 'content':_col.serialized_base}, safe=False)


def get_collection_ipixs(request, collection_id):
    _ipixs = m.Pix.objects.filter(pick__collection_id=collection_id)
    _ipixs = _ipixs.values_list('id', flat=True)
    return JsonResponse({'success':True, 'ids':list(_ipixs)}, safe=False)


def get_pick(request, pick_id):
    try:
        _pick = m.Pick.objects.get(pk=pick_id)
        return JsonResponse({'success':True, 'content':_pick.serialized}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


def remove_picks(request, collection_id, pick_ids):
    try:
        _pids = pick_ids.split(',')
        _picks = m.Pick.objects.filter(collection_id=collection_id, id__in=_pids)
        _picks.delete()
        return JsonResponse({'success':True, 'message':'picks removed successfully'}, safe=False)

    except:
        return JsonResponse({'success':False, 'message':'something wrong while removing picks'}, safe=False)

# def get_collection_seed(request, col_id):
#     try:
#         _col = m.Collection.objects.get(pk=col_id)
#         return JsonResponse({'success':True, 'content':_col.first_pick_serialized}, safe=False)
#
#     except:
#         return JsonResponse({'success':False}, safe=False)


def get_iposts(request, type):
    _iposts = m.Post.iposts(type)
    return JsonResponse({'success':True, 'idlist':list(_iposts)}, safe=False)


def get_mbti_iposts(request, type):
    _iposts = list(m.Post.mbti_iposts(type))
    # moiber.js와 sideb.js 둘다 사용하고 있어서,
    # idlist, ids 전부 보냈다
    return JsonResponse({'success':True, 'idlist':_iposts, 'ids':_iposts}, safe=False)


def mbtiresult_base(request, type):
    return render(request, 'getch/mbtiresult_base.html')


def get_post(request, post_id):
    try:
        _post = m.Post.objects.get_subclass(pk=post_id)

        # if _post.boo.hidden:
        #     print(_post.text)
        #     return JsonResponse({'success':False}, safe=False)

        # else:
        # print(_post.boo.hidden, '**********************************')
        _post = m.PostSerializer(_post).data
        return JsonResponse({'success':True, 'content':_post}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


def get_iboos(request, type):
    if type == 'hot':
        # _iboos = m.Flager.objects.filter(status=m.FOLLOW).values('object_id').annotate(nfollowers=Count('object_id')).order_by('-nfollowers')[:10].values_list('object_id', flat=True)

        ago_2w = datetime.now() - timedelta(days=7)
        _iboos = m.Post.objects.filter(created_at__gte=ago_2w).values('boo').annotate(nposts=Count('boo')).order_by('-nposts')[:10].values_list('boo', flat=True)
        return JsonResponse({'success':True, 'idlist':list(_iboos)}, safe=False)

    else:
        pass


def get_ibooposts(request, boo_id, type):
    try:
        _boo = m.Boo.objects.get(pk=boo_id)
        return JsonResponse({'success':True, 'idlist':_boo.iposts(type)}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


def get_ifollowers(request, boo_id):
    try:
        _boo = m.Boo.objects.get(pk=boo_id)
        # print('*********************', _boo.followers_id)
        return JsonResponse({'success':True, 'idlist':_boo.followers_id}, safe=False)

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


def get_baseboo(request, boo_id):
    try:
        _baseboo = m.Boo.objects.get(pk=boo_id)

        if request.user.is_authenticated and request.user.boo_set.filter(id=boo_id).exists():
            _baseboo = m.BooSerializer(_baseboo).data

        else:
            _baseboo = m.BasebooSerializer(_baseboo).data

        return JsonResponse({'success':True, 'content':_baseboo}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


def other_boos(request):
    return JsonResponse({'success':True, 'other_boos':request.user.other_boos}, safe=False)


def other_boos2(request):
    return JsonResponse({'success':True, 'other_boos':request.user.other_boos2}, safe=False)


def _labels_update(boo, labels):
    for k, v in labels.items():
        for _k, _v in v.items():
            if _k=='add':
                getattr(boo, k).add(*_v)
            if _k=='remove':
                getattr(boo, k).remove(*_v)

def boo_save(request):
    if request.method=='POST':
        print(request.POST, request.FILES)
        _on_creating = request.POST.get('on_creating', None)
        _labels = request.POST.get('labels', None)
        _boo_text = request.POST.get('boo_text', None)
        _boo_nick = request.POST.get('boo_nick', None)
        _profilepix = request.FILES.get('profilepix', None)

        try:
            # _on_creating이 있다면 그건 사실 문자열 'true' 이다
            # 그래도 if _on_creating 에서 걸러지기에, json.loads 처리를 안했다
            if _on_creating:
                boo = m.Boo.objects.create(user=request.user)
            else:
                boo = request.user.boo

            if _labels:
                _labels_update(boo, json.loads(_labels))

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

            if _on_creating:
                request.user.set_boo(boo.id)
                return JsonResponse({'success':True, 'boo_id':boo.id, 'message':'boo created successfully'}, safe=False)

            else:
                return JsonResponse({'success':True, 'message':'boo updated successfully'}, safe=False)

        except:
            return JsonResponse({'success':False, 'message':'something wrong while boo saving'}, safe=False)


def link_add(request):
    try:
        _url = request.POST.get('url', None)
        _link = m.Link.objects.create(user=request.user, url=_url)
        return JsonResponse({'success':True, 'link_id':_link.id, 'message':'link added successfully'}, safe=False)

    except:
        return JsonResponse({'success':False, 'message':'something wrong while link adding'}, safe=False)


def link_edit(request):
    try:
        _url = request.POST.get('url', None)
        _id = request.POST.get('id', None)
        _link = m.Link.objects.get(id=_id)
        _link.url = _url
        _link.save()
        return JsonResponse({'success':True, 'message':'link edited successfully'}, safe=False)

    except:
        return JsonResponse({'success':False, 'message':'something wrong while link editing'}, safe=False)


def link_delete(request, link_id):
    try:
        _link = m.Link.objects.get(id=link_id)
        _link.delete()
        return JsonResponse({'success':True, 'message':'link deleted successfully'}, safe=False)

    except:
        return JsonResponse({'success':False, 'message':'something wrong while link deleting'}, safe=False)


def vote(request, post_id):
    action = request.GET.get('action', None)
    # fit = session.fit #request.user.boo.fit
    # fit = request.user.boo.fit

    if action:
        post = m.Post.objects.get(pk=post_id)

        if request.user.is_authenticated:
            fit = request.user.boo.fit
            post.vote(int(action), request.user.boo)

        else:
            fit = []
            post.vote(int(action), m.Boo.guestboo, note=request.session.session_key)

        # post.vote(int(action), request.user.boo)
        # session.vote(post_id, action)
        return JsonResponse({'success':True, 'action':action, 'fit':fit}, safe=False)

    else:
        return JsonResponse({'success':False}, safe=False)


def create_collection(request, name):
    try:
        col = m.Collection.objects.create(owner=request.user.boo, name=name)
        return JsonResponse({'success':True, 'collection_id':col.id, 'message':'collection created successfully'}, safe=False)

    except:
        return JsonResponse({'success':False, 'message':'something wrong while creating collection'}, safe=False)


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

        if request.user.is_authenticated:
            comment.like(request.user.boo)

        else:
            comment.like(m.Boo.guestboo, note=request.session.session_key)

        return JsonResponse({'success':True, 'message':'Comment liked successfully'}, safe=False)

    except:
        return JsonResponse({'success':False, 'message':'Something wrong when liking comment'}, safe=False)


def delike_comment(request, comment_id):
    try:
        comment = m.Comment.objects.get(pk=comment_id)

        if request.user.is_authenticated:
            comment.delike(request.user.boo)

        else:
            comment.delike(m.Boo.guestboo, note=request.session.session_key)

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
        print(request.POST, request.FILES)
        post_id = request.POST.get('post_id', None)
        text = request.POST.get('text', None)
        id = request.POST.get('id', None)
        mention_id = request.POST.get('mention_id', None)
        attached = request.FILES.get('attached', None)
        # return

        # if text and post_id:
        if post_id:
            if id:
                comment = m.Comment.objects.get(pk=id)

                if text:
                    comment.text = text

                if mention_id:
                    comment.mention = m.Boo.objects.get(id=mention_id)

                comment.save()

            else:
                if request.user.is_authenticated:
                    comment = m.Comment(boo=request.user.boo, post_id=post_id)
                else:
                    comment = m.Comment(boo=m.Boo.guestboo, post_id=post_id)

                if text:
                    comment.text = text

                if mention_id:
                    comment.mention = m.Boo.objects.get(id=mention_id)
                    # comment = m.Comment.objects.create(boo=request.user.boo, post_id=post_id, text=text, mention_id=mention_id)

                # else:
                #     comment = m.Comment.objects.create(boo=request.user.boo, post_id=post_id, text=text)

                comment.save()

                if attached:
                    commentpix = m.Commentpix.objects.create(comment_id=comment.id, img=attached)


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



def search(request, keywords):
    n = 20
    # q = request.GET.get('q', None)

    try:
        vector = SearchVector('text', 'boo__nick', 'boo__text')
        query = SearchQuery(keywords)
        excl = Q(boo_id=m.BOO_DELETED) | Q(boo__hidden=True)
        _searched = m.Post.objects.exclude(excl).annotate(rank=SearchRank(vector, query)).order_by('-rank')[:n]
        # _searched = m.Post.objects.exclude(boo_id=m.BOO_DELETED).annotate(rank=SearchRank(vector, query)).order_by('-rank')[:n]
        # print(_searched)
        _searched = _searched.values_list('id', flat=True)
        return JsonResponse({'success':True, 'idlist':list(_searched), 'message':'searched successfully'}, safe=False)

    except:
        return JsonResponse({'success':False, 'message':'something wrong while searching'}, safe=False)


def search_by_pix(request, pix_id):
    # n = 50

    try:
        pix = m.Pix.objects.get(pk=pix_id)

        # _searched = m.Pix.objects.annotate(similarity=TrigramSimilarity('tokens', '나이키')).order_by('-similarity')
        # print(_searched, '**********************')
        vector = SearchVector('tokens')
        query = SearchQuery(pix.tokens)
        _searched = m.Pix.objects.exclude(id=pix.id).annotate(rank=SearchRank(vector, query)).exclude(rank=0).order_by('-rank')
        print(_searched.values('id','rank'))
        _searched = _searched.values_list('id', flat=True)
        return JsonResponse({'success':True, 'ids':list(_searched), 'message':'searched successfully'}, safe=False)

    except:
        return JsonResponse({'success':False, 'message':'something wrong while searching'}, safe=False)


def search_by_collection(request, collection_id):
    # n = 50

    try:
        pixs = m.Pix.objects.filter(pick__collection_id=collection_id).order_by('?')[:5]
        tokens = ' '.join(pixs.values_list('tokens', flat=True))
        # print(tokens)
        # return

        vector = SearchVector('tokens')
        query = SearchQuery(tokens)
        _searched = m.Pix.objects.exclude(pick__collection_id=collection_id).annotate(rank=SearchRank(vector, query)).exclude(rank=0).order_by('-rank')
        print(_searched.values('id','rank'))
        _searched = _searched.values_list('id', flat=True)

        _append = list(m.Pix.ipixs())
        random.shuffle(_append)
        _searched = list(_searched) + _append
        return JsonResponse({'success':True, 'ids':_searched, 'message':'searched successfully'}, safe=False)

    except:
        return JsonResponse({'success':False, 'message':'something wrong while searching'}, safe=False)


def search_by_keyword(request, keyword):
    try:
        _keyword = keyword
        vector = SearchVector('tokens', 'pick__collection__name', 'owner__nick')
        query = SearchQuery(_keyword)

        _searched = m.Pix.objects.annotate(rank=SearchRank(vector, query)).exclude(rank=0).order_by('-rank')#[:n]
        # print(_searched.values('id','rank'))
        _searched = _searched.values_list('id', flat=True)
        # print(_searched.values('id').distinct())

        _append = list(m.Pix.ipixs())
        random.shuffle(_append)
        _searched = list(_searched) + _append
        # _searched = _searched.union(_append)

        return JsonResponse({'success':True, 'ids':_searched, 'message':'searched successfully'}, safe=False)

    except:
        return JsonResponse({'success':False, 'message':'something wrong while searching'}, safe=False)


class Logout(LogoutView):
    def logout(self):
        super().logout()
        # print('---------------------------------------------', session)

# class Login(LoginView):
#     def login(self):
#         super().login()
#         print(session)

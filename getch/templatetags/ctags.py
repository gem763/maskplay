import getch.models as m
from django_currentuser.middleware import get_current_user, get_current_authenticated_user
from django import template
register = template.Library()

@register.filter
def score_unitize(score):
    return round(float(score)/10)


@register.filter
def boo_regroup(boos):
    boo_list = list(boos)

    if (len(boo_list) % 2) == 1:
        boo_list.append(None)

    return [boo_list[i:i+2] for i in range(0, len(boo_list), 2)]


# 요거는 안쓴다: post.voted를 @property로 만들었다
@register.filter
def voted(post, user):#boo_id):
    # print(type(post))
    # print('up vote: ', post.votes.user_ids(action=0))
    # print('down vote: ', post.votes.user_ids(action=1))

    # return post.voted(boo_id)

    try:
        return post.voted(user.boo.pk)

    except:
        return None

@register.filter
def pix_src(post, field):
    return getattr(post, field).url

# @register.simple_tag
# def tag_test():
#     kkk = get_current_user()
#     return kkk.boo.nick;

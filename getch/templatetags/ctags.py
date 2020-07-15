import getch.models as m
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


@register.filter
def voted_by(post, boo_id):
    # post = m.Post.objects.get(pk=post_id)

    print(type(post))
    print('up vote: ', post.votes.user_ids(action=0))
    print('down vote: ', post.votes.user_ids(action=1))

    return post.voted(boo_id)

from django.contrib import admin
import getch.models as m
from django.db.models import Q
import os


@admin.register(m.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['boo', 'text', 'post']


@admin.register(m.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['type', 'boo', 'text', 'nvotes_up', 'nvotes_down', 'ncomments', 'created_at']

    def type(self, obj):
        return obj.cast.type


@admin.register(m.PostVoteAB)
class PostVoteABAdmin(admin.ModelAdmin):
    list_display = ['boo', 'text', 'pixlabel_a', 'pixlabel_b', 'nvotes_up', 'nvotes_down']


@admin.register(m.PostVoteOX)
class PostVoteOXAdmin(admin.ModelAdmin):
    list_display = ['boo', 'text', 'keys', 'nvotes_up', 'nvotes_down']


@admin.register(m.PostQA)
class PostQAAdmin(admin.ModelAdmin):
    list_display = ['boo', 'text']


@admin.register(m.User)
class UserAdmin(admin.ModelAdmin):
    class BooInline(admin.TabularInline):
        model = m.Boo
        fk_name = 'user'

    inlines = ( BooInline, )
    list_display = ['email', 'boo_selected', 'boo']
    list_display_links = ['email']
    list_editable = ['boo_selected']


@admin.register(m.Profile)
class ProfileAdmin(admin.ModelAdmin):
    # list_display = ['pix_name', 'boo']
    list_display = ['pix', 'boo']
    list_display_links = ['boo'] #['pix_name']

    # def pix_name(self, obj):
    #     return os.path.basename(obj.pix.name)


@admin.register(m.Boo)
class BooAdmin(admin.ModelAdmin):
    list_display = ['user', 'nick', 'selected', 'active', 'hidden', 'is_staff', 'text', 'nposts', 'ncomments', 'nfollowers', 'nfollowees', 'nvotes', 'nlikes_comment']
    list_display_links = ['user']
    list_filter = ['user'] # admin 페이지 오른쪽에 필터메뉴 있다
    list_editable = ['nick']
    list_per_page = 20

    def selected(self, obj):
        return obj.user.boo_selected == obj.id

    def is_staff(self, obj):
        return obj.user.is_staff

    selected.boolean = True
    is_staff.boolean = True

    # def n_posts(self, obj):
    #     return obj.post_set.count()
    #
    # def n_comments(self, obj):
    #     return obj.comment_set.count()
    #
    # def n_followers(self, obj):
    #     return obj.get_flags(status=m.FOLLOW).count()
    #
    # def n_followees(self, obj):
    #     return m.Flager.objects.filter(status=m.FOLLOW, user=obj).count()
    #
    # def n_votes(self, obj):
    #     q = Q(status=m.VOTE_UP) | Q(status=m.VOTE_DOWN)
    #     return m.Flager.objects.filter(q, user=obj).count()


class LabelAdmin(admin.ModelAdmin):
    list_display = ['label', 'key']
    list_editable = ['key']

@admin.register(m.Genderlabel)
class GenderlabelAdmin(LabelAdmin):
    pass

@admin.register(m.Agelabel)
class AgelabelAdmin(LabelAdmin):
    pass

@admin.register(m.Stylelabel)
class StylelabelAdmin(LabelAdmin):
    pass

@admin.register(m.Bodylabel)
class BodylabelAdmin(LabelAdmin):
    pass

@admin.register(m.Itemlabel)
class ItemlabelAdmin(LabelAdmin):
    pass

@admin.register(m.Postpix)
class PostpixAdmin(admin.ModelAdmin):
    list_display = ['key', 'owner', 'post', 'img', 'desc', 'tokens']

@admin.register(m.Commentpix)
class CommentpixAdmin(admin.ModelAdmin):
    list_display = ['comment', 'img']

# @admin.register(m.Notif)
# class NotifAdmin(admin.ModelAdmin):
#     pass

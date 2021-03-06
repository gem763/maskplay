from django.contrib import admin
import getch.models as m
from django.db.models import Q
import os


@admin.register(m.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['boo', 'text', 'post']


@admin.register(m.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['type', 'boo', 'text', 'nvotes_up', 'nvotes_down']

    def type(self, obj):
        return obj.cast.type


@admin.register(m.PostVoteAB)
class PostVoteABAdmin(admin.ModelAdmin):
    list_display = ['boo', 'text', 'pixlabel_a', 'pixlabel_b', 'nvotes_up', 'nvotes_down']


@admin.register(m.PostVoteOX)
class PostVoteOXAdmin(admin.ModelAdmin):
    list_display = ['boo', 'text', 'keys', 'nvotes_up', 'nvotes_down']


@admin.register(m.User)
class UserAdmin(admin.ModelAdmin):
    class BooInline(admin.TabularInline):
        model = m.Boo
        fk_name = 'user'

    inlines = ( BooInline, )
    list_display = ['email', 'boo_selected', 'boo']
    list_display_links = ['email']
    list_editable = ['boo_selected']


# @admin.register(m.MaskBase)
# class MaskBaseAdmin(admin.ModelAdmin):
#     list_display = ['type', 'category', 'pix_name']
#     list_display_links = ['pix_name']
#     list_editable = ['category']
#
#     def pix_name(self, obj):
#         return os.path.basename(obj.pix.name)
#
#
# @admin.register(m.EyeMask)
# class EyeMaskAdmin(admin.ModelAdmin):
#     list_display = ['maskbase', 'owned_by', 'masked', 'top', 'left', 'width', 'height']
#     list_display_links = ['maskbase']
#     list_editable = ['top', 'left', 'width', 'height']
#
#     def owned_by(self, obj):
#         if obj.profile and obj.profile.boo:
#             return obj.profile.boo
#         else:
#             return None
#
#
# @admin.register(m.MouthMask)
# class MouthMaskAdmin(admin.ModelAdmin):
#     list_display = ['maskbase', 'owned_by', 'masked', 'top', 'left', 'width', 'height']
#     list_display_links = ['maskbase']
#     list_editable = ['top', 'left', 'width', 'height']
#
#     def owned_by(self, obj):
#         if obj.profile and obj.profile.boo:
#             return obj.profile.boo
#         else:
#             return None
#
#
# @admin.register(m.Character)
# class CharacterAdmin(admin.ModelAdmin):
#     list_display = ['category', 'pix_name']
#     list_display_links = ['pix_name']
#
#     def pix_name(self, obj):
#         return os.path.basename(obj.pix.name)


@admin.register(m.Profile)
class ProfileAdmin(admin.ModelAdmin):
    # list_display = ['type', 'pix_name', 'owned_by', 'eyemask', 'mouthmask']
    list_display = ['pix_name', 'boo']
    list_display_links = ['pix_name']

    # def owned_by(self, obj):
    #     if obj.boo:
    #         return obj.boo
    #     else:
    #         return None

    def pix_name(self, obj):
        return os.path.basename(obj.pix.name)


@admin.register(m.Boo)
class BooAdmin(admin.ModelAdmin):
    # list_display = ['user', 'nick', 'key', 'selected', 'text', 'nposts', 'nfollowers', 'profile']
    list_display = ['user', 'nick', 'selected', 'text', 'n_posts', 'n_comments', 'n_followers', 'n_followees', 'n_votes']
    list_display_links = ['user']
    list_filter = ['user'] # admin 페이지 오른쪽에 필터메뉴 있다
    list_editable = ['nick']

    def n_posts(self, obj):
        return obj.post_set.count()

    def n_comments(self, obj):
        return obj.comment_set.count()

    def n_followers(self, obj):
        return obj.get_flags(status=m.FOLLOW).count()

    def n_followees(self, obj):
        return m.Flager.objects.filter(status=m.FOLLOW, user=obj).count()

    def n_votes(self, obj):
        q = Q(status=m.VOTE_UP) | Q(status=m.VOTE_DOWN)
        return m.Flager.objects.filter(q, user=obj).count()


@admin.register(m.Styletag)
class StyletagAdmin(admin.ModelAdmin):
    pass


@admin.register(m.Fashiontem)
class FashiontemAdmin(admin.ModelAdmin):
    pass

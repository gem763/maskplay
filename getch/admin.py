from django.contrib import admin
import getch.models as m
import os
# from vote.models import VoteModel


# admin.site.register(m.Post)
# admin.site.register(m.PostVoteAB)
# admin.site.register(m.PostVoteOX)
#
#
# @admin.register(m.User)
# class UserAdmin(admin.ModelAdmin):
#     class BooInline(admin.TabularInline):
#         model = m.Boo
#         fk_name = 'user'
#
#     inlines = ( BooInline, )
#     list_display = ['email', 'boo_selected', 'boo']
#     list_display_links = ['email']
#     list_editable = ['boo_selected']


# @admin.register(m.Boo)
# class BooAdmin(admin.ModelAdmin):
#     list_display = ['user', 'nick', 'text', 'profile']
#     list_display_links = ['user']
#     list_filter = ['user'] # admin 페이지 오른쪽에 필터메뉴 있다
#     # list_editable = ['profile']


@admin.register(m.MaskBase)
class MaskBaseAdmin(admin.ModelAdmin):
    list_display = ['type', 'category', 'pix_name']
    list_display_links = ['pix_name']
    # list_editable = ['category']

    def pix_name(self, obj):
        return os.path.basename(obj.pix.name)


@admin.register(m.Mask)
class MaskAdmin(admin.ModelAdmin):
    list_display = ['maskbase', 'top', 'left', 'width', 'height']
    list_display_links = ['maskbase']


@admin.register(m.Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass
    # list_display = ['type', 'pix_name', 'eye_mask', 'mouth_mask']
    # list_display_links = ['pix_name']
    #
    # def pix_name(self, obj):
    #     return os.path.basename(obj.pix.name)

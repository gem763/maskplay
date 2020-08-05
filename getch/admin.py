from django.contrib import admin
# from getch.models import User
import getch.models as m
# from vote.models import VoteModel


admin.site.register(m.Profile)
admin.site.register(m.Post)
admin.site.register(m.PostVoteAB)
admin.site.register(m.PostVoteOX)
admin.site.register(m.Mask)
admin.site.register(m.MaskBase)


class BooInline(admin.TabularInline):
    model = m.Boo
    fk_name = 'user'


class UserAdmin(admin.ModelAdmin):
    inlines = [
        BooInline,
    ]


class ProfileInline(admin.TabularInline):
    model = m.Profile
    fk_name = 'boo'


class BooAdmin(admin.ModelAdmin):
    inlines = [
        ProfileInline,
    ]


# class MaskInline(admin.TabularInline):
#     model = m.Mask
#     fk_name = 'profile'
#
#
# class ProfileAdmin(admin.ModelAdmin):
#     inlines = [
#         MaskInline,
#     ]

admin.site.register(m.User, UserAdmin)
admin.site.register(m.Boo, BooAdmin)
# admin.site.register(m.Profile, ProfileAdmin)

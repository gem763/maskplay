from django.contrib import admin
# from getch.models import User
import getch.models as m
# from vote.models import VoteModel


admin.site.register(m.Profile)
admin.site.register(m.Post)
admin.site.register(m.PostVoteAB)
admin.site.register(m.PostVoteOX)


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


admin.site.register(m.User, UserAdmin)
admin.site.register(m.Boo, BooAdmin)

from django.contrib import admin
import moiberlab.models as m

# Register your models here.


@admin.register(m.User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(m.Feed)
class FeedAdmin(admin.ModelAdmin):
    pass

@admin.register(m.Post)
class PostAdmin(admin.ModelAdmin):
    pass

@admin.register(m.Store)
class StoreAdmin(admin.ModelAdmin):
    pass

@admin.register(m.Pix)
class PixAdmin(admin.ModelAdmin):
    pass

@admin.register(m.Pixtag)
class PixtagAdmin(admin.ModelAdmin):
    pass

@admin.register(m.MobileVerifier)
class MobileVerifierAdmin(admin.ModelAdmin):
    pass

@admin.register(m.Brand)
class BrandAdmin(admin.ModelAdmin):
    pass

@admin.register(m.Survey)
class SurveyAdmin(admin.ModelAdmin):
    pass

@admin.register(m.SurveyRecord)
class SurveyRecordAdmin(admin.ModelAdmin):
    pass

@admin.register(m.Balancegame)
class BalancegameAdmin(admin.ModelAdmin):
    pass

@admin.register(m.BalancegameRecord)
class BalancegameRecordAdmin(admin.ModelAdmin):
    pass

@admin.register(m.Flashgame)
class FlashgameAdmin(admin.ModelAdmin):
    pass

@admin.register(m.FlashgameRecord)
class FlashgameRecordAdmin(admin.ModelAdmin):
    pass

@admin.register(m.Comment)
class CommentAdmin(admin.ModelAdmin):
    pass

@admin.register(m.Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    pass

@admin.register(m.Follow)
class FollowAdmin(admin.ModelAdmin):
    pass

@admin.register(m.Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    pass

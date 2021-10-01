from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin
import getch.models as m
from django.db import models
from django.db.models import Q
from django.utils.safestring import mark_safe
from getch.forms import ResearchItemForm
from imagekit.admin import AdminThumbnail

#https://github.com/jmrivas86/django-json-widget
from django_json_widget.widgets import JSONEditorWidget
from django.contrib.admin.widgets import AdminFileWidget
from django.template.loader import render_to_string
# from django.contrib.sessions.models import Session
# import pprint
import os
from datetime import datetime





class AdminpixPreviewWidget(AdminFileWidget):
    template_name = "admin/adminpix_preview.html"

    class Media:
        js = [
            "//code.jquery.com/jquery-3.4.1.min.js",
            'sideb/adminpix_preview.js'
        ]


@admin.register(m.Notihistory)
class NotihistoryAdmin(admin.ModelAdmin):
    list_display = ['transaction', 'ordercode', 'created_at', 'slacked', 'mobiled', 'emailed']
    raw_id_fields = ('transaction', )


@admin.register(m.Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ['whose_type', 'whose', 'n_transaction', 'inflow', 'outflow', 'amount']


@admin.register(m.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'when', 'type', 'amount']
    list_per_page = 20
    list_select_related = (
        'sender','sender__boo','sender__boo__user','sender__raffle','sender__raffle__item','sender__support','sender__support__brand','sender__shoptem','sender__shoptem__item','sender__coffeecoupon','sender__coffeecoupon__item',
        'receiver','receiver__boo','receiver__boo__user','receiver__raffle','receiver__raffle__item','receiver__support','receiver__support__brand','receiver__shoptem','receiver__shoptem__item','receiver__coffeecoupon','receiver__coffeecoupon__item', )

    raw_id_fields = ('sender', 'receiver', )
    list_filter = ('type', )

    def who(self, wallet):
        if hasattr(wallet, 'boo'):
            return wallet.boo.user

        elif hasattr(wallet, 'raffle'):
            return wallet.raffle.item

        elif hasattr(wallet, 'support'):
            return wallet.support.brand

    def sender_who(self, obj):
        return self.who(obj.sender)

        # return obj.sender.whose

    def receiver_who(self, obj):
        return self.who(obj.receiver)


@admin.register(m.Support)
class SupportAdmin(admin.ModelAdmin):
    list_display = ['brand', 'active', 'due', 'ticketsize', 'target', 'gift_preview']
    list_editable = ['active']

    def gift_preview(self, obj):
        if obj.gift.pix_wide:
            return mark_safe('<img src="{}" style="height:33px;width:100px;object-fit:cover;" />'.format(obj.gift.pix_wide.url))
        return mark_safe('<img src="{}" style="height:100px;width:100px;object-fit:cover;" />'.format(obj.gift.pix_0.url))

        # if obj.gift and obj.gift.pix_0:
        #     return mark_safe('<img src="{}" style="height:100px;width:100px;object-fit:cover;" />'.format(obj.gift.pix_0.url))
        # return ""


@admin.register(m.Raffle)
class RaffleAdmin(admin.ModelAdmin):
    list_display = ['item', 'listing', 'deduction', 'due', 'item_preview']
    list_editable = ['listing']

    def item_preview(self, obj):
        if obj.item.pix_wide:
            return mark_safe('<img src="{}" style="height:33px;width:100px;object-fit:cover;" />'.format(obj.item.pix_wide.url))
        return mark_safe('<img src="{}" style="height:33px;width:100px;object-fit:cover;" />'.format(obj.item.pix_0.url))


@admin.register(m.Coffeecoupon)
class CoffeecouponAdmin(admin.ModelAdmin):
    list_display = ['item', 'listing', 'item_preview']
    list_editable = ['listing']
    raw_id_fields = ('wallet', )
    exclude = ('wallet',)

    def item_preview(self, obj):
        return mark_safe('<img src="{}" style="height:100px;width:100px;object-fit:cover;" />'.format(obj.item.pix_0.url))


@admin.register(m.Shoptem)
class ShoptemAdmin(admin.ModelAdmin):
    list_display = ['item', 'listing', 'item_preview']
    list_editable = ['listing']
    raw_id_fields = ('wallet', )
    exclude = ('wallet',)

    def item_preview(self, obj):
        return mark_safe('<img src="{}" style="height:100px;width:100px;object-fit:cover;" />'.format(obj.item.pix_0.url))


@admin.register(m.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'out_of_stock', 'pix_0_preview']
    list_editable = ['out_of_stock']
    formfield_overrides = { models.ImageField: {'widget': AdminpixPreviewWidget} }

    def pix_0_preview(self, obj):
        return mark_safe('<img src="{}" style="height:100px;width:100px;object-fit:cover;" />'.format(obj.pix_0.url))


@admin.register(m.Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name_en', 'name_kr', 'established', 'origin', 'logo_preview']
    formfield_overrides = { models.ImageField: {'widget': AdminpixPreviewWidget} }

    def logo_preview(self, obj):
        return obj.logo_preview

    # def get_context(self, name, value, attrs):
    #     context = super().get_context(name, value, attrs)
    #     context['img_id'] = 'img_' + str(datetime.now().timestamp()).replace('.', '_')
    #     context['fn_name'] = 'fn_' + str(datetime.now().timestamp()).replace('.', '_')
    #     return context

# class AdminImageWidget(AdminFileWidget):
#     def render(self, name, value, attrs=None, renderer=None):
#         print(name, value, attrs)
#         output = []
#         if value and getattr(value, "url", None):
#             image_url = value.url
#             file_name = str(value)
#             output.append(
#                 '<a href="{}" target="_blank"><img src="{}" alt="{}" style="max-height: 200px;"/></a>'.
#                     format(image_url, image_url, file_name))
#         output.append(super().render(name, value, attrs))
#         return mark_safe(u''.join(output))


@admin.register(m.Flashgame)
class Flashgame(admin.ModelAdmin):
    list_display = ['type', 'gender', 'text', 'published', 'pub_date']
    list_editable = ['published']
    exclude = ['created_at']
    formfield_overrides = { models.ImageField: {'widget': AdminpixPreviewWidget} }


@admin.register(m.Flashgametag)
class Flashgametag(admin.ModelAdmin):
    list_display = ['on', 'who', 'answer']
    # list_editable = ['answer']
    raw_id_fields = ('on', 'who', )


@admin.register(m.ResearchItem)
class ResearchItemAdmin(admin.ModelAdmin):
    list_display = ['research', 'order', 'type', 'gender', 'preq', 'text']
    list_editable = ['order']
    formfield_overrides = { models.ImageField: {'widget': AdminpixPreviewWidget} }
    # form = ResearchItemForm

    fieldsets = (
        (None, {
            'fields': ('research','order','type','gender','preq','text',),
            'classes': ('predefined',)
        }),
        ('PIX 0', {
            'fields': ('pix_0','pixlabel_0',),
            'classes': ('pix_0',)
        }),
        ('PIX 1', {
            'fields': ('pix_1','pixlabel_1',),
            'classes': ('pix_1',)
        }),
        ('MULTICHOICES', {
            'fields': ('mcpix_0','mclabel_0','mcpix_1','mclabel_1','mcpix_2','mclabel_2','mcpix_3','mclabel_3','mcpix_4','mclabel_4','mcpix_5','mclabel_5','mcpix_6','mclabel_6','mcpix_7','mclabel_7','mcpix_8','mclabel_8','mcpix_9','mclabel_9','mcpix_10','mclabel_10','mcpix_11','mclabel_11',),
            'classes': ('mc',)
        }),
    )

    class Media:
        js = ('//code.jquery.com/jquery-3.4.1.min.js', 'sideb/researchitem.js',)



@admin.register(m.Research)
class ResearchAdmin(admin.ModelAdmin):
    class ResearchItemInline(admin.StackedInline):
        model = m.ResearchItem
        fk_name = 'research'
        # exclude = ['created_at']
        extra = 0
        min_num = 0
        ordering = ['order']
        formfield_overrides = { models.ImageField: {'widget': AdminpixPreviewWidget} }

        fieldsets = (
            (None, {
                'fields': ('order','type','gender','preq','text',),
                'classes': ('predefined',)
            }),
            (None, {
                'fields': ('pix_0','pixlabel_0',),
                'classes': ('pix_0',)
            }),
            (None, {
                'fields': ('pix_1','pixlabel_1',),
                'classes': ('pix_1',)
            }),
            (None, {
                'fields': ('mcpix_0','mclabel_0','mcpix_1','mclabel_1','mcpix_2','mclabel_2','mcpix_3','mclabel_3','mcpix_4','mclabel_4','mcpix_5','mclabel_5','mcpix_6','mclabel_6','mcpix_7','mclabel_7','mcpix_8','mclabel_8','mcpix_9','mclabel_9','mcpix_10','mclabel_10','mcpix_11','mclabel_11',),
                'classes': ('mc',)
            }),
        )

        class Media:
            js = ('//code.jquery.com/jquery-3.4.1.min.js', 'sideb/researchitem.js',)


    def coverpix_preview(self, obj):
        return obj.coverpix_preview

    inlines = ( ResearchItemInline, )
    list_display = ['title', 'owner', 'brand', 'published', 'reward', 'due', 'priority', 'time_required', 'coverpix_preview']
    list_editable = ['published', 'priority', 'time_required']
    raw_id_fields = ('owner', 'brand', )
    formfield_overrides = { models.ImageField: {'widget': AdminpixPreviewWidget} }
    # readonly_fields = ('coverpix_thumbnail',)
    # coverpix_thumbnail = AdminThumbnail(image_field='coverpix', template='admin/coverpix_preview.html')


@admin.register(m.Contentwork)
class ContentWorkAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }

    list_display = ['agenda', 'owner']


@admin.register(m.Postage)
class PostageAdmin(admin.ModelAdmin):
    list_display = ['contentwork', 'order', 'group', 'text']
    list_editable = ['order', 'group']


@admin.register(m.Identity)
class IdentityAdmin(admin.ModelAdmin):
    list_display = ['name', 'keywords']


@admin.register(m.Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ['boo', 'date', 'nomore_today', 'n_collected', 'n_voted', 'collect_reward', 'vote_reward', 'checkin_reward', 'bonus_reward']
    list_filter = ['boo__user']
    raw_id_fields = ('boo', )
    #
    # def user(self, obj):
    #     return obj.boo.user

@admin.register(m.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['boo', 'text', 'post']


@admin.register(m.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['type', 'boo', 'text', 'group', 'nvotes_up', 'nvotes_down', 'ncomments', 'created_at']

    def type(self, obj):
        return obj.cast.type


@admin.register(m.PostVoteAB)
class PostVoteABAdmin(admin.ModelAdmin):
    list_display = ['boo', 'text', 'created_at', 'pixlabel_a', 'pixlabel_b', 'nvotes_up', 'nvotes_down']


@admin.register(m.PostVoteOX)
class PostVoteOXAdmin(admin.ModelAdmin):
    list_display = ['boo', 'text', 'created_at', 'keys', 'nvotes_up', 'nvotes_down']


@admin.register(m.PostQA)
class PostQAAdmin(admin.ModelAdmin):
    list_display = ['boo', 'text', 'pix', 'created_at']


@admin.register(m.MobileVerifier)
class MobileVerifierAdmin(admin.ModelAdmin):
    list_display = ['mobile', 'authkey']


@admin.register(m.User)
class UserAdmin(admin.ModelAdmin):
    class BooInline(admin.TabularInline):
        model = m.Boo
        fk_name = 'user'

    inlines = ( BooInline, )
    list_display = ['email', 'name', 'gender', 'birth', 'mobile', 'mobile_verified', 'address', 'is_superuser', 'is_staff', 'help', 'boo_selected', 'boo', 'date_joined']
    list_display_links = ['email']
    list_editable = ['boo_selected', 'is_superuser', 'is_staff', 'mobile_verified', 'help']
    search_fields = ('email', )
    list_per_page = 20


@admin.register(m.Profile)
class ProfileAdmin(admin.ModelAdmin):
    # list_display = ['pix_name', 'boo']
    list_display = ['pix', 'boo']
    list_display_links = ['boo'] #['pix_name']

    # def pix_name(self, obj):
    #     return os.path.basename(obj.pix.name)


@admin.register(m.Boo)
class BooAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }

    list_display = ['user', 'nick', 'selected', 'active', 'hidden', 'coltagged', 'text', 'ncollections']
    list_display_links = ['user']
    list_filter = ['user'] # admin 페이지 오른쪽에 필터메뉴 있다
    list_editable = ['nick', 'coltagged']
    search_fields = ('nick', )
    list_per_page = 20

    def selected(self, obj):
        return obj.user.boo_selected == obj.id

    # def is_staff(self, obj):
    #     return obj.user.is_staff

    selected.boolean = True


# @admin.register(m.Guestboo)
# class GuestbooAdmin(admin.ModelAdmin):
#     list_display = ['nick', 'text', 'nposts', 'ncomments', 'nfollowers', 'nfollowees', 'nvotes', 'nlikes_comment']
#     list_display_links = ['nick']
#     exclude = ['user', 'genderlabels', 'agelabels', 'bodylabels', 'stylelabels', 'itemlabels', 'active', 'hidden', 'links']


class LabelAdmin(admin.ModelAdmin):
    list_display = ['label', 'key', 'pix_preview']
    list_editable = ['key']
    formfield_overrides = { models.ImageField: {'widget': AdminpixPreviewWidget} }

    def pix_preview(self, obj):
        if obj.pix:
            return mark_safe('<img src="{}" style="height:100px;width:100px;object-fit:cover;" />'.format(obj.pix.url))


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


@admin.register(m.BalancegameRecord)
class BalancegameRecordAdmin(admin.ModelAdmin):
    list_display = ['who', 'pix_0_id', 'pix_1_id', 'chosen']
    raw_id_fields = ('who', 'pix_0', 'pix_1', )
    list_per_page = 20


@admin.register(m.Pix)
class PixAdmin(admin.ModelAdmin):
    list_display = ['owner', 'desc', 'tokens', 'tokens_ko', 'outlink', 'type', 'preview']
    raw_id_fields = ('owner', )
    list_editable = ['type']
    search_fields = ('owner__nick', 'tokens', 'tokens_ko', )
    list_per_page = 20

    def preview(self, obj):
        return obj.preview


@admin.register(m.Collection)
class CollectionAdmin(OrderedModelAdmin):
    list_display = ['name', 'owner', 'desc', 'npicks', 'move_up_down_links']
    # list_filter = ['owner']

@admin.register(m.Pick)
class PickAdmin(OrderedModelAdmin):
    list_display = ['id', 'collection', 'pix', 'move_up_down_links']
    search_fields = ['collection', 'pix']
    # list_filter = ['collection']


@admin.register(m.Commentpix)
class CommentpixAdmin(admin.ModelAdmin):
    list_display = ['comment', 'img']

@admin.register(m.Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ['user', 'url']

# @admin.register(m.Session)
# class SessionAdmin(admin.ModelAdmin):
#     list_display = ['sessionkey', 'user', 'view', 'checkin', 'checkout']

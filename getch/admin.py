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
    list_display = ['title', 'owner', 'brand', 'published', 'reward', 'due', 'coverpix_preview']
    list_editable = ['published']
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


@admin.register(m.User)
class UserAdmin(admin.ModelAdmin):
    class BooInline(admin.TabularInline):
        model = m.Boo
        fk_name = 'user'

    inlines = ( BooInline, )
    list_display = ['email', 'is_superuser', 'boo_selected', 'boo']
    list_display_links = ['email']
    list_editable = ['boo_selected', 'is_superuser']


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

    # list_display = ['user', 'nick', 'selected', 'active', 'hidden', 'is_staff', 'text', 'nposts', 'ncomments', 'nfollowers', 'nfollowees', 'nvotes', 'nlikes_comment']
    # list_display = ['user', 'nick', 'selected', 'active', 'hidden', 'is_staff', 'text', 'nposts', 'ncomments', 'nfollowers', 'nfollowees', 'nvotes', 'nlikes_comment', 'ncollections']
    # list_display = ['user', 'nick', 'selected', 'active', 'hidden', 'coltagged', 'is_staff', 'text', 'ncollections']
    list_display = ['user', 'nick', 'selected', 'active', 'hidden', 'coltagged', 'text', 'ncollections']
    list_display_links = ['user']
    list_filter = ['user'] # admin 페이지 오른쪽에 필터메뉴 있다
    list_editable = ['nick', 'coltagged']
    list_per_page = 20

    def selected(self, obj):
        return obj.user.boo_selected == obj.id

    # def is_staff(self, obj):
    #     return obj.user.is_staff

    selected.boolean = True
    # is_staff.boolean = True


# @admin.register(m.Guestboo)
# class GuestbooAdmin(admin.ModelAdmin):
#     list_display = ['nick', 'text', 'nposts', 'ncomments', 'nfollowers', 'nfollowees', 'nvotes', 'nlikes_comment']
#     list_display_links = ['nick']
#     exclude = ['user', 'genderlabels', 'agelabels', 'bodylabels', 'stylelabels', 'itemlabels', 'active', 'hidden', 'links']


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


@admin.register(m.Pix)
class PixAdmin(admin.ModelAdmin):
    list_display = ['owner', 'desc', 'tokens', 'outlink']

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






# {
#     "강남": {
#         "bestmatch": "제주도",
#         "worstmatch": "테헤란",
#         "phrase": "이렇게 멋진 날 봐! 짜릿해! 늘 새로워!",
#         "desc": "멀리서도 한 눈에 들어오는 당신은 강남스타일!\n 주목받는 것을 좋아하고 화려한 옷을 선호하는 당신은\n 기본템을 사더라도 비비드한 컬러를 선택하는 편이네요.\n 에너지 넘치는 당신은 멋쟁이 패셔니스타!",
#         "desc_best": "힙플? 피크닉?\n 어디든 말만해!\n 스타일링의 고수 제주도 스타일과 함께라면, 우리가 가는 곳이 휴가지!",
#         "desc_worst": "무슨 면접보러 가냐고!\n 세련이라 쓰고 경직이라 읽는다. 테헤란 스타일? 아, 나랑 안맞아.."
#     },
#
#     "이태원": {
#         "bestmatch": "청담",
#         "worstmatch": "강남",
#         "phrase": "유행을 쫓는 건 NO!",
#         "desc": "확고한 나만의 스타일을 쫓는 당신은 이태원스타일!\n 취향에 맞춰 자유자재로 멋을 부릴 줄 아는 당신은\n 새로운 트렌드를 이끄는 멋쟁이군요.\n 개성파 패셔니스타인 당신은 개척자 스타일!",
#         "desc_best": "오 역시,\n 뭘 좀 아는데?\n 걸어다니는 런웨이 청담과 힙스터 이태원은 의외로 꽤 잘 맞는 궁합!",
#         "desc_worst": "어 그래..(할많하않)\n 트랜드 계의 소문난 충신 강남만 만나면 꿈틀대는 내 안의 시어머니 본능? (소오름)"
#     },
#
#     "청담": {
#         "bestmatch": "테헤란",
#         "worstmatch": "노량진",
#         "phrase": "럭셔리의 중심!",
#         "desc": "세련미 넘치는 스타일을 좋아하는 당신은 청담스타일!\n 품위있는 차림에도 앞선 감각의 개성과 패션 위트를 잃지 않는 당신은\n 새로운 트렌드에 언제나 민감하게 반응하는 패셔니스타이군요.\n 기품 있는 이미지를 뽐내는 당신은 하이앤드 스타일!",
#         "desc_best": "네트워킹? 콜!\n 댄디한 테헤란과 세련된 청담은 시크한 듯 다정한 한쌍!",
#         "desc_worst": "진짜로 그거,\n 돈 주고 샀다고?\n 셋업? 그게 먼데? 하는 노량진은 정말 진짜 레알 찐으로.."
#     },
#
#     "노량진": {
#         "bestmatch": "여의도",
#         "worstmatch": "제주도",
#         "phrase": "유행? 그게 뭐야?",
#         "desc": "패션에 별 관심이 없는 당신은 노량진스타일!\n 다른 것에 신경쓰느라 패션 스타일은 뒷전이 되는 경우가 많은 당신은\n 항상 같은 패션을 고수해도 별로 신경쓰지 않습니다.\n 아직 패린이에 머물고 있는 당신은 논 패션 스타일!",
#         "desc_best": "오오 번듯한데?\n 후리한 노량진과 깔끔한 여의도는 닮은 듯 안 닮은 듯 의외의 찰떡 궁합!",
#         "desc_worst": "왜 절엄?\n 어딜가나 인증샷 남길 것 같은 제주도 스타일? 피곤하다 피곤해.."
#     },
#
#     "제주도": {
#         "bestmatch": "판교",
#         "worstmatch": "여의도",
#         "phrase": "샤랄랄라랄랄라~~~",
#         "desc": "언제 어디서든 여행을 떠날 수 있을 것 같은 당신은 제주도스타일!\n 꾸안꾸가 유행할 때도 꿋꿋하게 ‘꾸꾸꾸’를 추구하는 당신은\n 뛰어난 패션센스로 중무장한 멋쟁이군요.\n 화려한 옷차림을 선호하는 당신은 휴양지 스타일!",
#         "desc_best": "stay hungry,\n stay foolish!\n 꾸안꾸지만 뭔가 앞선 듯 한. 판교 스타일, 좀 멋진데?",
#         "desc_worst": "집에 와이셔츠 밖에 없어?\n 여의도는 왜 일평생 모나미룩이에요? 왜 그러는지 아시는 분?"
#     },
#
#     "테헤란": {
#         "bestmatch": "이태원",
#         "worstmatch": "판교",
#         "phrase": "깔끔! 세련! 시크!",
#         "desc": "멋지게 차려입는 당신은 테헤란스타일!\n 깔끔하고 단정한 옷차림으로 시크하고 세련된 분위기를 내는 당신은\n 영화 <킹스맨>을 떠올리게 하는 멋쟁이군요.\n 지적인 이미지를 봄내는 당신은 시크댄디 스타일!",
#         "desc_best": "(힐끗) 나름 멋진데?\n 과한듯 힙한듯, 따라하진 않아도 참조는 하고 싶은 이태원의 유니크함.",
#         "desc_worst": "그러고 미팅하고 왔다고?\n 이해는 안되지만 뭐 그러려니 하게 되는, 맞는 듯 안맞는 듯 판교 스타일.."
#     },
#
#     "여의도": {
#         "bestmatch": "강남",
#         "worstmatch": "이태원",
#         "phrase": "깔끔! 단정!",
#         "desc": "지적이고 세련된 분위기를 좋아하는 당신은 여의도스타일!\n 직장환경에 따라 딱딱해 보이는 모습을 보일 때도 있는 당신은\n 개별 상황에 맞춰 단정하게 입는 것을 선호하는군요.\n 화려함보다는 품위있는 차림을 선호하는 당신은 도시적인 스타일!",
#         "desc_best": "역시 강남 스타일!\n 강남 스타일에서 베어 나오는 트랜디함은 언젠가 따라하고 싶은 워너비 스타일!",
#         "desc_worst": "넌 참 유니크해!\n (이태원에게) 그래그래.. 너도 무슨 사정이 (생각이) 있겠지.. 그래그래."
#     },
#
#     "판교": {
#         "bestmatch": "노량진",
#         "worstmatch": "청담",
#         "phrase": "Simple is the Best!",
#         "desc": "미니멀룩을 추구하는 당신은 판교스타일!\n 심플하고 편안한 스타일을 좋아하는 당신은\n 꾸밈없이 멋을 낼 줄 아는 사람이군요.\n 있는 그대로의 모습을 보여주는 당신은 미니멀리스트 스타일!",
#         "desc_best": "편안함으로 대동단결!\n 노량진만 보면 기분이 좋읍니다 '야, 너두 나처럼 될 수 있어!'",
#         "desc_worst": "안 불편한가?\n 청담의 하이패션 스타일은 언제봐도 노이해.. 왜 굳이.."
#     },
# }

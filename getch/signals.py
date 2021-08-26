from allauth.socialaccount.signals import social_account_updated, pre_social_login
from allauth.account.signals import user_signed_up, user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.account.utils import perform_login
from allauth.utils import get_user_model
from allauth.exceptions import ImmediateHttpResponse
from django.shortcuts import redirect
from django.conf import settings
from notifications.signals import notify



# @receiver(post_save, sender=User)
# def user_post_save(sender, instance, created, **kwargs):
#     if created:
#         instance.init_user()


# @receiver(social_account_updated)
# def allauth_social_account_updated(request, sociallogin, **kwargs):
#     # https://github.com/pennersr/django-allauth/blob/master/allauth/socialaccount/models.py
#     # user_signed_up 이후 user_logged_in이 자동호출된다
#     # 따라서 user_logged_in에서 set_social_avatar()를 하면 해당 기능이 두번 실행된다
#     sociallogin.user.set_default_avatar()
#
#
# @receiver(user_logged_in)
# def allauth_user_logged_in(request, user, **kwargs):
#     notify.send(request.user, recipient=request.user, verb='have just logged in')
#     print(user)


# @receiver(user_signed_up)
# def allauth_user_signed_up(request, user, **kwargs):
    # request.signed_up = True
    # user.signed_up = True
    # notify.send(user, recipient=user, verb='signed up')


@receiver(pre_social_login)
def allauth_user_pre_social_login(request, sociallogin, **kwargs):
    # print(sociallogin.user.email)

    User = get_user_model()
    users = User.objects.filter(email=sociallogin.user.email)

    if users:
        # print(users)
        # allauth.account.app_settings.EmailVerificationMethod
        perform_login(request, users[0], email_verification='optional')
        raise ImmediateHttpResponse(redirect(settings.LOGIN_REDIRECT_URL))
        # raise ImmediateHttpResponse(redirect(sociallogin.get_redirect_url(request)))

    # else:
    #     print('***********************')

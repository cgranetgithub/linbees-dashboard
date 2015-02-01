from django.utils.translation import ugettext, ugettext_lazy as _

register_but_ws_does_not_exist = _(
u"""It seems that your company, %(workspace)s, has not registered yet. You will be able to create your an account once your company is registered.""")

public_email_not_allowed = _(
u"""We do not support email addresses from public email providers (such as %(domain)s). You need to have your own company email domain. If you do not have one, please contact us, we will find a solution!""")

ws_already_exist = _(u"""There is already a dashboard with that name. Someone in your company has created it. Please contact that person.""")

existing_email = _(u"""A user with that email already exists.""")

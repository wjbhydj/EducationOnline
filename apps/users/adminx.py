import xadmin
from .models import EmailVerifyRecord, Banner
from xadmin import views


class BaseSetting(object):

    enable_themes = True
    use_bootswatch = True


class GlobalSetting(object):

    site_title = 'NBA管理后台系统'
    site_footer = '科比的公司'
    menu_style = 'accordion'

class EmailVerifyRecordXadmin(object):
    list_display = ['code', 'email', 'send_type','send_time']
    search_fields = ['code', 'email', 'send_time']
    list_filter = ['code', 'email', 'send_type','send_time']


class BannerXadmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index', 'add_time']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']



xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordXadmin)
xadmin.site.register(Banner, BannerXadmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)
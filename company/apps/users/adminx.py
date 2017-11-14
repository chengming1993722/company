import xadmin
from .models import EmailVerifyRecord,Banner
from xadmin import views

class EmailVerifyRecordAdmin(object):
    pass


class BannerAdmin(object):
    list_display=('title','url','index')

class BaseSetting(object):
    enable_themes=True
    user_bootswatch=True
#设置xadmin页面标题和页脚
class GlobalSetting(object):
    site_title='西游记'
    site_footer='咨询在线'
xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSetting)


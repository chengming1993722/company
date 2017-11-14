"""company URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
import xadmin
from  django.views.generic import TemplateView
#在没有创建试图之前在django.views.gengeric中导入TemplateView建立前后台连接
from users.views import user_login,user_register,active_user,forget_pwd,reset_pwd,modify_pwd,user_logout
from organizations.views import OrgList
from django.conf.urls.static import static
from company.settings import MEDIA_ROOT,MEDIA_URL,STATIC_ROOT
from django.views.static import serve
urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$',TemplateView.as_view(template_name='index.html'),name='index'),
                              #试图连接                        #name地址别名
    url(r'^login/$',user_login.as_view(),name='login'),
    url(r'^logout/$',user_logout.as_view(),name='logout'),
    url(r'^register/$',user_register.as_view(),name='register'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$',active_user.as_view(),name="active"),
    url(r'^forgetpwd/$',forget_pwd.as_view(),name='forget'),
    url(r'^reset/(?P<reset_code>.*)/$',reset_pwd.as_view(),name="reset"),
    url(r'^modify/$',modify_pwd.as_view(),name="modify"),
    url(r'^org/',include('organizations.urls',namespace='org')),
                                                #在网页中使用
    url(r'^course/',include('courses.urls',namespace='course')),
    # media的url配置，图片上传的url路径
    url(r'media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    # 当debug=False时，自行处理static内容
    url(r'static/(?P<path>.*)$', serve, {"document_root": STATIC_ROOT})

]+static(MEDIA_URL,document_root=MEDIA_ROOT)
# 全局404
handler404 = 'users.views.page_no_found'
# 全局500
handler500 = 'users.views.page_error'
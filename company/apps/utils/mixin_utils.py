from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
#定义判断用户是否登录

class LoginRequireMixin(object):

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequireMixin, self).dispatch(request, *args, **kwargs)
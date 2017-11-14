from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from .models import UserProfile,EmailVerifyRecord
from django.db.models import Q
from django.views.generic import View
from .forms import Login_form,Register_form,ForgetPwd_form,Reset_form
from django.contrib.auth.hashers import make_password
from utils.send_mail import register_send_mail
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user=UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except:
            return None
# 重新定义authenticate
class user_login(View):
    def get(self,request):
        return render(request,'login.html')
    def post(self,request):
        user_name = request.POST.get('username', '')
        pass_word = request.POST.get('password', '')
        login_form=Login_form(request.POST)
        if login_form.is_valid():
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    #如果用户激活就登录用户
                    from django.core.urlresolvers import reverse
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request,'login.html',{"msg":"用户未注册"})
            else:
                return render(request,'login.html',{"msg": "用户名或者密码错误"})
        else:
            return render(request,'login.html',{"login_form":login_form})


class user_register(View):
    def get(self,request):
        register_form=Register_form()
        return render(request,'register.html',{"register_form":register_form})
    def post(self,request):
        register_form=Register_form(request.POST)
        if register_form.is_valid():
            email=request.POST.get("email","")
            password=request.POST.get("password","")
            if UserProfile.objects.filter(email=email):
                return render(request, "register.html", {'msg': '该用户已经被注册。', 'register_form': register_form})
            user_profile=UserProfile()
            user_profile.email=email
            user_profile.username=email
            user_profile.is_active=False
            user_profile.password=make_password(password)
                                        #密文保存密码
            user_profile.save()
            register_send_mail(email,send_type="register")
            return render(request,"login.html")
        else:
            return render(request,"register.html",{"register_form":register_form})


class active_user(View):
    def get(self,request,active_code):
                        # ulr 中<active_code>
        email_recode=EmailVerifyRecord.objects.filter(code=active_code)
        if email_recode:
            for recode in email_recode:
                user=UserProfile.objects.get(email=recode.email)
                user.is_active=True
                user.save()
            return render(request,"login.html")
        else:
            return render(request,"active_faild.html")


class forget_pwd(View):
    def get(self,request):
        forgetpwd_form=ForgetPwd_form()
        return render(request,"forgetpwd.html",{"forgetpwd_form":forgetpwd_form})

    def post(self,request):
        forgetpwd_form=ForgetPwd_form(request.POST)
        if forgetpwd_form.is_valid():
            email=request.POST.get("email","")
            emailExists=UserProfile.objects.filter(email=email).count()
            if emailExists==0:
                error='{"account":"邮箱不存在"}'
            else:
                register_send_mail(email,send_type="forget")
                error='{"status":"success"}'
            return HttpResponse(error,content_type='application/json')
        else:
            return HttpResponse({"captcha_f":"验证码不正确"},content_type='application/json')


class reset_pwd(View):
    def get(self,request,reset_code):
        emailVerify=EmailVerifyRecord.objects.get(code=reset_code)
        email=emailVerify.email
        return render(request,"password_reset.html",{"email":email})


class modify_pwd(View):
    def post(self,request):
        reset_form=Reset_form(request.POST)
        if reset_form.is_valid():
            pwd1=request.POST.get("paaaword1","")
            pwd2=request.POST.get("paaaword2","")
            email=request.POST.get("email","")
            if pwd2==pwd1:
                user=UserProfile.objects.get(email=email)
                user.password=make_password(pwd1)
                user.save()
                return render(request,"login.html")
            else:
                return render(request,"password_reset.html",{"msg":"两次密码不一致","email":email})
        else:
            return render(request,"password_reset.html",{"msg":"输入有误"})


class user_logout(View):
    def get(self,request):
        logout(request)
        from django.core.urlresolvers import reverse
        return HttpResponseRedirect(reverse('index'))

def page_no_found(request):
    """
    全局404
    :param request:
    :return:
    """
    from django.shortcuts import render_to_response
    response = render_to_response("404.html", {})
    response.status_code = 404
    return response

def page_error(request):
    """
    全局500
    :param request:
    :return:
    """
    from django.shortcuts import render_to_response
    response = render_to_response("500.html", {})
    response.status_code = 500
    return response

# def user_login(request):
#     if request.method=='GET':
#         return render(request,'login.html')
#     elif request.method=="POST":
#         user_name=request.POST.get('username','')
#         pass_word=request.POST.get('password','')
#         user=authenticate(username=user_name,password=pass_word)
#         if user is not None:
#             login(request,user)
#             return render(request,'index.html')
#         else:
#             return render(request,'login.html',{"msg":"用户名或者密码错误"})

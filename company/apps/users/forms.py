from django import forms
from captcha.fields import CaptchaField
class Login_form(forms.Form):
    username=forms.CharField(required=True)
    password=forms.CharField(required=True,min_length=5,error_messages={"invalid":"不能少于5个字"})

class Register_form(forms.Form):
    email=forms.EmailField(required=True)
    password=forms.CharField(required=True,min_length=5)
    captcha = CaptchaField(error_messages={"isvalid":"验证码有误"})


class ForgetPwd_form(forms.Form):
    email=forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"isvalid":"验证码有误"})


class Reset_form(forms.Form):
    password1=forms.CharField(required=True,min_length=5)
    password2=forms.CharField(required=True,min_length=5)
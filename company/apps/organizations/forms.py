from django import forms
from operations.models import UserAsk
import re


class UserAskFrom(forms.ModelForm):
                   # 直接继承指定model的指定字段字段
    class Meta:
        model = UserAsk
        fields=['name','mobile','coursename',]
    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError("手机号码非法", code="mobile_invalid")
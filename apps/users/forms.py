__author__ = 'jingyuan'
__date__ = '2020/5/10 17:35'

from django import forms
from captcha.fields import CaptchaField
import redis

from MxOnline.settings import yp_apikey, REDIS_HOST, REDIS_PORT
from apps.users.models import UserProfile

class RegisterPostForm(forms.Form):
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    code = forms.CharField(required=True, min_length=4, max_length=4)
    password = forms.CharField(required=True)

    def clean_mobile(self):
        mobile = self.data.get("mobile")
        #验证手机号码是否已经注册
        user = UserProfile.objects.filter(mobile=mobile)
        if user:
            raise forms.ValidationError("手机号码已注册")
        return mobile


    def clean_code(self):
        mobile = self.data.get("mobile")
        code = self.data.get("code")
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8", decode_responses=True)
        redis_code = r.get(str(mobile))
        if code != redis_code:
            raise forms.ValidationError("验证码不正确")
        return code


class RegisterGetForm(forms.Form):
    captcha = CaptchaField()


class LoginForm(forms.Form):
    username = forms.CharField(required=True, min_length=2)
    password = forms.CharField(required=True,min_length=3)


class DynamicLoginForm(forms.Form):
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    captcha = CaptchaField()


class DynamicLoginPostForm(forms.Form):
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    code = forms.CharField(required=True, min_length=4, max_length=4)

    def clean_code(self):
        mobile = self.data.get("mobile")
        code = self.data.get("code")
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8", decode_responses=True)
        redis_code = r.get(str(mobile))
        if code != redis_code:
            raise forms.ValidationError("验证码不正确")
        return self.cleaned_data

    # def clean(self):
    #     mobile = self.cleaned_data["mobile"]
    #     code = self.cleaned_data["code"]
    #     redis_code = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8", decode_responses=True)
    #     redis_code.get(str(mobile))
    #     if code != redis_code:
    #         raise forms.ValidationError("验证码不正确")
    #     return self.cleaned_data

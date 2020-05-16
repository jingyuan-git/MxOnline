from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
import redis

from apps.users.forms import LoginForm, DynamicLoginForm, DynamicLoginPostForm
from apps.users.forms import RegisterGetForm, RegisterPostForm
from apps.utils.YunPian import send_single_sms
from MxOnline.settings import yp_apikey, REDIS_HOST, REDIS_PORT
from apps.utils.random_str import generate_random
from apps.users.models import UserProfile

# Create your views here.

class RegisterView(View):
    def get(self, request, *args, **kwargs):
        register_get_form = RegisterGetForm()
        return render(request, "register.html", {
            "register_get_form": register_get_form
        })

    def post(self, request, *args, **kwargs):
        register_post_form = RegisterPostForm(request.POST)
        dynamic_login = True
        if register_post_form.is_valid():
            mobile = register_post_form.cleaned_data["mobile"]
            password = register_post_form.cleaned_data["password"]
            #新建用户
            user = UserProfile(username=mobile)
            user.set_password(password)
            user.mobile = mobile
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            register_get_form = RegisterGetForm()
            return render(request, "register.html", {
                "register_get_form": register_get_form, # 有图片验证码
                "register_post_form":register_post_form,# 有错误的信息
            })



class DynamicLoginView(View):
    def post(self, request, *args, **kwargs):
        login_form = DynamicLoginPostForm(request.POST)
        dynamic_login = True
        if login_form.is_valid():
            #没有注册账号依然可以登陆
            mobile = login_form.cleaned_data["mobile"]
            # code = login_form.cleaned_data["code"]

            existed_users = UserProfile.objects.filter(mobile=mobile)
            if existed_users:
                user = existed_users[0]
            else:
                #新建用户
                user = UserProfile(username=mobile)
                password = generate_random(10, 2)
                user.set_password(password)
                user.mobile = mobile
                user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            d_form = DynamicLoginForm()
            return render(request, "login.html", {"login_form":login_form,
                                                  "d_form":d_form,
                                                  "dynamic_login":dynamic_login})


class SendSmsView(View):
    def post(self, request, *args, **kwargs):
        send_sms_form = DynamicLoginForm(request.POST)
        re_dict = {}
        if send_sms_form.is_valid():
            mobile = send_sms_form.cleaned_data["mobile"]
            code = generate_random(4, 0)
            re_json = send_single_sms(yp_apikey, code, mobile=mobile)
            if re_json["code"] == 0:
                re_dict["status"] = "success"
                r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8", decode_responses=True)
                r.set(str(mobile), code)
                r.expire(str(mobile), 60*5) #设置验证码5分钟过期
            else:
                re_dict["msg"] = re_json["msg"]
        else:
            for key, value in send_sms_form.errors.items():
                re_dict[key] = value[0]
        return JsonResponse(re_dict)



class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))

        login_form = DynamicLoginForm()
        return render(request, "login.html", {
            "login_form":login_form
        })

    def post(self, request, *args, **kwargs):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            # user_name = request.POST.get("username", "")
            # password = request.POST.get("password", "")

            # if not user_name:
            #     return render(request, "login.html", {"msg":"请输入用户名"})
            # if not password:
            #     return render(request, "login.html", {"msg":"请输入密码"})
            # if len(password)<3:
            #     return render(request, "login.html", {"msg":"密码格式不正确"})
            #通过用户和密码查询用户是否存在
            user = authenticate(username=user_name, password=password)
            # from apps.users.models import UserProfile
            # #1.通过用户名查询到用户
            # #2.先加密在通过加密后的密码查询
            # user = UserProfile.objects.get(username=user_name, password=password)
            if user is not None:
                #查询到用户
                login(request, user)
                #登陆成功之后怎么返回页面
                return HttpResponseRedirect(reverse('index'))
            else:
                return render(request, "login.html", {"msg":"用户名或密码错误"})
        else:
            #未查询到用户
            return render(request, "login.html", {"login_form":login_form})
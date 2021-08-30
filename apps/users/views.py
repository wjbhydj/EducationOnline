from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.views.generic.base import View
from django.db.models import Q
from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForms, RegisterForms
from django.contrib.auth.hashers import make_password
from utils.email_send import send_register_email

# Create your views here.

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):

        login_form = LoginForms(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return render(request, 'index.html')
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误', 'login_form':login_form})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForms()
        return render(request, 'register.html', {'register_form':register_form})

    def post(self, request):
        register_form = RegisterForms()
        if register_form.is_valid():
            username = request.POST.get('email', None)
            if UserProfile.objects.filter(email=username):
                return render(request, 'register.html', {'register_form':register_form,'msg':'用户已存在'})
            password = request.POST.get('password', None)
            user_profile = UserProfile()
            user_profile.username = username
            user_profile.email = username
            user_profile.is_active = False

            user_profile.password = make_password(password)
            user_profile.save()
            send_register_email(username, 'register')
            return render(request, 'login.html')
        return render(request, 'register.html', {'register_form':register_form})


class ActiveUserView(View):
    def get(self, request, active_code):
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        if all_record:
            for record in all_record:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')
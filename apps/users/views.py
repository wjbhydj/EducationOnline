import json

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.views.generic.base import View
from django.db.models import Q
from .models import UserProfile, EmailVerifyRecord, Banner
from organization.models import CourseOrg, Teacher
from operation.models import UserCourse, UserFavorite, Course, UserMessage
from .forms import LoginForms, RegisterForms, ForgetPwdForms, ModifyPwdForms, UserUploadImageForms, UserInfoForms
from django.contrib.auth.hashers import make_password
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from pure_pagination import Paginator, PageNotAnInteger
from django.shortcuts import render_to_response

def page_not_found(request):
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response

def page_errors(request):
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response

class LoginUnsafeView(View):
    def get(self, request):
        return render(request, "login.html", {})
    def post(self, request):
        user_name = request.POST.get("username", "")
        pass_word = request.POST.get("password", "")

        import MySQLdb
        conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='123456', db='eduonline', charset='utf8')
        cursor = conn.cursor()
        sql_select = "select * from users_userprofile where email='{0}' and password='{1}'".format(user_name, pass_word)
        print("++++: %s"%sql_select)
        result = cursor.execute(sql_select)
        print('result: %s'%result)
        # print(cursor.fetchall())
        for row in cursor.fetchall():
            print(row)
            # 查询到用户
            pass
        print('-------test-------')

# Create your views here.
class IndexView(View):
    """首页"""
    def get(self, request):
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            'all_banners':all_banners,
            'courses':courses,
            'banner_courses':banner_courses,
            'course_orgs':course_orgs,
        })

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
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'login.html', {'msg': '用户名或密码错误', 'login_form': login_form})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误', 'login_form': login_form})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForms()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForms()
        if register_form.is_valid():
            username = request.POST.get('email', None)
            if UserProfile.objects.filter(email=username):
                return render(request, 'register.html', {'register_form': register_form, 'msg': '用户已存在'})
            password = request.POST.get('password', None)
            user_profile = UserProfile()
            user_profile.username = username
            user_profile.email = username
            user_profile.is_active = False

            user_profile.password = make_password(password)
            user_profile.save()
            send_register_email(username, 'register')
            return render(request, 'login.html')
        return render(request, 'register.html', {'register_form': register_form})


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


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetPwdForms()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetPwdForms(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', None)
            send_register_email(email, 'forget')
            return render(request, 'send_sucess.html')
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetPwdView(View):
    def get(self, request, active_code):
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        if all_record:
            for record in all_record:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForms()
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'msg': '密码不一致！'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
            return render(request, 'login.html')
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'modify_form': modify_form, 'email': email})


class UserInfoView(LoginRequiredMixin, View):
    """用户中心页"""

    def get(self, request):
        return render(request, 'usercenter-info.html', {})

    def post(self, request):
        user_info_form = UserInfoForms(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse({'status':'success'}, 'application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), 'application/json')


class UserUploadImageView(LoginRequiredMixin, View):
    """用户头像上传"""

    def post(self, request):
        user_upload_iamge_form = UserUploadImageForms(request.POST, request.FILES)
        if user_upload_iamge_form.is_valid():
            image = user_upload_iamge_form.cleaned_data['image']
            request.user.image = image
            request.user.save()
            return HttpResponse({'status': 'success'}, content_type='application/json')
        else:
            return HttpResponse({'status': 'fail'}, content_type='application/json')


class UserUpdatePwdView(LoginRequiredMixin, View):
    """用户更新密码"""

    def post(self, request):
        modify_pwd_form = ModifyPwdForms(request.POST)
        if modify_pwd_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return HttpResponse({'status': 'fail', 'msg': '密码不一致'}, content_type='application/json')
            user = request.user
            user.password = make_password(pwd1)
            user.save()
            return HttpResponse({'status': 'success'}, content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_pwd_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    """发送邮箱验证码"""
    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return HttpResponse({'email':'邮箱已存在'}, content_type='application/json')

        send_register_email(email, 'update_email')
        return HttpResponse({'status':'success'}, content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    """用户修改邮箱"""
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')

        exist_record = EmailVerifyRecord(email=email, code=code, send_type='update_email')
        if exist_record:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse({'status':'success'}, content_type='application/json')
        else:
            return HttpResponse({'status':'fail'}, content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):
    """用户课程"""
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            'user_courses':user_courses,
        })


class MyFavOrgView(LoginRequiredMixin, View):
    """我收藏的课程机构"""
    def get(self, request):
        org_lists = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org = CourseOrg.objects.get(id=fav_org.fav_id)
            org_lists.append(org)
        return render(request, 'usercenter-fav-org.html',{
            'org_lists':org_lists
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    """我收藏的教师"""
    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher = Teacher.objects.get(id=fav_teacher.fav_id)
            teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            'teacher_list': teacher_list,
        })


class MyFavCourseView(LoginRequiredMixin, View):
    """我收藏的课程"""
    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request, 'usercenter-fav-course.html', {
            'course_list':course_list,
        })


class MyMessageView(LoginRequiredMixin, View):
    """我的消息"""
    def get(self, request):
        all_message = UserMessage.objects.filter(user=request.user.id)

        try:
            page = request.GET.get('page', '1')
        except PageNotAnInteger:
            page =1
        p = Paginator(all_message, 2, request=request)
        messages = p.page(page)
        return render(request, 'usercenter-message.html', {
            'messages':messages,
        })


class LogoutView(View):
    """用户登出"""
    def get(self, request):
        logout(request)
        from django.urls import reverse
        return HttpResponseRedirect(reverse('index'))

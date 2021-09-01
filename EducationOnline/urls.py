"""EducationOnline URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetPwdView, ModifyPwdView
import xadmin

from django.views.static import serve
from django.conf.urls.static import static
from EducationOnline import settings

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'index/', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'login/',LoginView.as_view(), name='login'),
    url(r'register/', RegisterView.as_view(), name='register'),
    url(r'captcha/', include('captcha.urls')),
    url(r'active/(?P<active_code>.*)/', ActiveUserView.as_view(), name='user_active'),
    url(r'forget/', ForgetPwdView.as_view(), name='forget_pwd'),
    url(r'reset/(?P<active_code>.*)/', ResetPwdView.as_view(), name='reset_pwd'),
    url(r'modify_pwd/', ModifyPwdView.as_view(), name='modify_pwd'),
    url(r'org/', include('organization.urls', namespace='organization')),
    url(r'course/', include('course.urls', namespace='course')),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)   #重点

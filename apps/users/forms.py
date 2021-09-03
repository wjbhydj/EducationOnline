
from django import forms
from captcha.fields import CaptchaField
from .models import UserProfile

class LoginForms(forms.Form):

    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForms(forms.Form):

    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={'invalid':'验证码错误'})


class ForgetPwdForms(forms.Form):

    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid':'验证码错误'})


class ModifyPwdForms(forms.Form):

    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


class UserUploadImageForms(forms.ModelForm):
    """用户更改图像"""
    class Meta:
        model = UserProfile
        fields = ['image']


class UserInfoForms(forms.ModelForm):
    """用户中心信息"""
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'gender', 'birthday', 'address', 'mobile']
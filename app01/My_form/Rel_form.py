from django.db import models
from django import forms
from app01 import models

class rel_form(forms.Form):
    username = forms.CharField(label="用户名",max_length=5,min_length=2,
                               error_messages={
                                   "max_length":"用户名最多不能超过5位",
                                   "min_length":"用户名最少2位",
                                   "required":"用户名不能为空"
                               },
                                widget=forms.widgets.TextInput(attrs={"class":"form-control"}),
                               )

    password = forms.CharField(label="密码",max_length=9,min_length=5,
                               error_messages={
                                   "max_length":"密码最多不能超过5位",
                                   "min_length":"密码最少2位",
                                   "required":"密码不能为空"
                               },
                                widget=forms.widgets.PasswordInput(attrs={"class":"form-control"}),
                               )

    confirm_password = forms.CharField(label="重复密码",max_length=9,min_length=5,
                               error_messages={
                                   "max_length":"确认密码最多不能超过5位",
                                   "min_length":"确认密码最少2位",
                                   "required":"确认密码不能为空"
                               },
                                widget=forms.widgets.PasswordInput(attrs={"class":"form-control"}),
                               )

    email = forms.EmailField(label="邮箱",
                             error_messages={
                                 "required":"邮箱不能为空",
                                 'lnvalid':"邮箱格式不正确"
                             },
                             widget=forms.widgets.EmailInput(attrs={"class":"form-control"}))

#   局部钩子函数
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if models.UserInfo.objects.filter(username=username):
            self.add_error("username","用户名已 存在")
        return username

#   全局钩子
    def clean(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if not password == confirm_password:
            self.error_class("confirm_password","两次密码输入不一致")
        return self.cleaned_data
"""new_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from app01 import views
from django.conf.urls import url

from django.views.static import serve
from new_django import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registon.html',views.registon,name="reg"),
    path('login/',views.login,name='login'),
    path('home/',views.home),
    re_path(r"^U_or_D/",views.U_or_D),
    path("comment/",views.comment),
    # url(r'^(?P<username>\w+)/$',views.site,name="site")

    # 后台管理页面
    path("backend/",views.backend),
    # 添加文章功能
    path("article_add/",views.article_add),

    #图片url地址
    path('img_lo/',views.img_lo),
    #修改密码
    path('set_pwd/',views.set_pwd,name='id_pwd'),
    #退出登录(消除用户信息）
    path("logout",views.logout,name="logout"),

    re_path(r'^(?P<username>\w+)/$',views.site,name="site"),  #个人站点搭建

    # re_path(r'^(?P<username>\w+)/article/(?P<article_id>\d+.*)/',views.article_obj),   #文章分类详情页

    url(r'^(?P<username>\w+)/(?P<condition>category|tag|article)/(?P<param>.*)/',views.site,),
    # path('media/(?p<path>.*)',serve,{'document_root':settings.MEDIA_ROOT})

    url(r'^(?P<username>\w+)/P/(?P<userinfo_id>\d+.*)/',views.My_art,),  #个人文章展示

url(r'^media/(?P<path>.*)', serve, {"document_root":settings.MEDIA_ROOT}),
]


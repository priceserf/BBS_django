from django.shortcuts import render
import pymysql
from django.shortcuts import redirect,HttpResponse
from django.http import JsonResponse
from app01 import models
from app01.My_form.Rel_form import rel_form
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import TruncMonth
import json
from django.db.models import F
# 注册功能
def registon(request):
    back_dic = {"code": 200, "msg": ""}
    if request.method == "GET":
        form_obj = rel_form()
    else:
        form_obj = rel_form(request.POST)
        print(form_obj.is_valid())
        if form_obj.is_valid():
            clean_data=form_obj.cleaned_data    #{'username': 'sada', 'password': '123456', 'confirm_password': '123456', 'email': '123@qq.com'}
            clean_data.pop("confirm_password")
                #获取图片键值对
            file_obj=request.FILES.get('avatar')
            if file_obj:
                clean_data['avatar']=file_obj
            models.UserInfo.objects.create_user(**clean_data)
            back_dic['url']='/login/'         #回调函数，将url传到ajax中的url中，进行跳转
        else:
            # print(123)
            back_dic['code']=2000
            back_dic['msg']=form_obj.errors


        return JsonResponse(back_dic)

    return render(request,"registon.html",{"form_obj":form_obj})

#登录功能
# @csrf_exempt
def login(request):
    back_dic={"code":200,"msg":''}
    # print(123)
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        code = request.POST.get("code")
        print(code)
        if request.session.get("code").upper() == code.upper():     #校验验证码是否正确
            # 校验用户名和密码是否正确
            ret = auth.authenticate(request,username=username,password=password)
            if ret:
                auth.login(request,ret)     #将用户数据存储起来
                back_dic['url']="/home/"
                # print(132)
            else:
                back_dic['code']=2000,
                back_dic['msg']="用户名或密码错误"
        else:
            back_dic['code']=3000
            back_dic['msg']="验证码错误"
        return JsonResponse(back_dic)

    return render(request,"login.html")

# 产生验证码
from PIL import Image,ImageDraw,ImageFont
from io import BytesIO
import random
def get_random():
    return random.randint(0,255),random.randint(0,255),random.randint(0,255)
def img_lo(request):
    # 产生一个图片

    img_obj = Image.new("RGB",(300,35),get_random())
    img_draw = ImageDraw.Draw(img_obj)            #创建一个画笔
    img_font = ImageFont.truetype("static/font/111.ttf",30)

#   产生随机验证码
    code = ""
    for i in range(5):
        random_upp = chr(random.randint(65,90))
        random_lower = chr(random.randint(97,122))
        random_int = str(random.randint(1,9))

        tmp = random.choice([random_upp,random_lower,random_int])

#       将每个字都写在图片上
        img_draw.text((i*25+60,0),tmp,fill=get_random(),font=img_font)

        # 拼接字体
        code += tmp
    # print(code)

  # 将验证码存储起来
    code = "".join(code)
    request.session['code']=code
    # print(request.session.get['code'])

  # 将验证码放入一个内存中暂时保存起来
    io_obj=BytesIO()            #内存管理器对象
    img_obj.save(io_obj,'png')      #以png格式保存
    data=io_obj.getvalue()
    return HttpResponse(data)

@login_required
#修改密码
def set_pwd(request):
    back_dic={"code":200,"msg":""}
    if request.is_ajax():
        if request.method == "POST":
            # print(123)
            oldpassword = request.POST.get("oldpassword")
            newpassword = request.POST.get("newpassword")
            confiepwd   = request.POST.get("confiepwd")
            is_right = request.user.check_password(oldpassword)     #判断旧密码是否正确
            if is_right:
                if newpassword == confiepwd:
                    request.user.set_password(newpassword)
                    request.user.save()
                    back_dic['msg']='修改成功'
                else:
                    back_dic['code']=403
                    back_dic['msg']="两次密码不一致"
            else:
                back_dic['code'] = 300
                back_dic['msg'] = "原密码错误"

        return JsonResponse(back_dic)

@login_required
def logout(request):
    auth.logout(request)
    return redirect("/login/")


# home界面
def home(request):
    Art_obj = models.Article.objects.all()
    return render(request,"home.html",locals())

# 个人站点
def site(request,username,**kwargs):
    ret=models.UserInfo.objects.filter(username=username).first()
    if not ret:
        return render(request,"404.html")
    blog = ret.blog     #拿到用户所关联的站点
    article_obj =models.Article.objects.filter(blog=blog)   #拿到每个用户所有文章内容
    if kwargs:
        print(kwargs)   #{'condition': 'tag', 'param': '1'}
        condition = kwargs.get("condition")
        param = kwargs.get("param")
        if condition == "category":
            article_obj = article_obj.filter(Category_id=param)
        elif condition == "tag":
            article_obj = article_obj.filter(tags__id=param)
        else:
            year,month = param.split("-")
            article_obj = article_obj.filter(create_time__year=year,create_time__month=month)


    # 拿到当前用户的文章分类以及每个分类下文章数
    art_list = models.Category.objects.filter(blog=blog).annotate(art_num=Count("article__pk")).values_list("name","art_num")

    # 拿到当前用户的标签分类以及每个分类下的文章数
    tag_list = models.Tag.objects.filter(blog=blog).annotate(tag_num=Count("article__pk")).values_list("name","tag_num")

    # 拿到文章创建事时间，用官网的方法去做
    tim_list=models.Article.objects.filter(blog=blog).annotate(month=TruncMonth("create_time")).values("month").annotate(time_num=Count("pk")).values_list("month","time_num")
    # print(tim_list)
    return render(request,'site.html',locals())

# 文章详情页展示
# def article_obj(request,username,article_id):
#     pass
# 个人文章展示栏
def My_art(request,username,userinfo_id):
    """
    判断username和id是否1存在
    :param request:
    :param username:
    :param username_id:
    :return:
    """
    ret = models.UserInfo.objects.filter(username=username).first()
    #  拿到对应用户的文章
    article_obj = models.Article.objects.filter(pk=userinfo_id,blog__userinfo__username=username).first()
    blog = ret.blog
    if not article_obj:
        return render(request,"404.html")
    # 拿到当前用户的文章分类以及每个分类下文章数
    art_list = models.Category.objects.filter(blog=blog).annotate(art_num=Count("article__pk")).values_list("name","art_num")

    # 拿到当前用户的标签分类以及每个分类下的文章数
    tag_list = models.Tag.objects.filter(blog=blog).annotate(tag_num=Count("article__pk")).values_list("name","tag_num")

    # 拿到文章创建事时间，用官网的方法去做
    tim_list=models.Article.objects.filter(blog=blog).annotate(month=TruncMonth("create_time")).values("month").annotate(time_num=Count("pk")).values_list("month","time_num")

    # 获取所有的评论内容
    comment_list = models.Comment.objects.filter(article=article_obj)
    # print(comment_list.comment)

    return render(request,"My_art.html",locals())


# 评论功能
def comment(request):
    if request.is_ajax():
        back_dic={"code":200,"msg":""}
        if request.method=='POST':
            if request.user.is_authenticated:
                comment = request.POST.get("comment")
                article_id = request.POST.get("article_id")
                parent_id = request.POST.get("parentID")
    #           将数据放入两个表之中
                models.Article.objects.filter(pk=article_id).update(comment_name=F("comment_name")+1)
                models.Comment.objects.create(user=request.user,article_id=article_id,content=comment,parent_id=parent_id)
                back_dic["msg"]="评论成功"
            else:
                back_dic["code"]=201
                back_dic["msg"]="用户未登陆"
        return JsonResponse(back_dic)


#点赞点踩功能
from django.db.models import F
def U_or_D(request):
    if request.is_ajax():
        back_dic = {"code":200,"msg":""}
        # 判断用户是否登录
        if request.user.is_authenticated:
            article_id = request.POST.get("article_id")
            is_up = request.POST.get("is_up")
            is_up = json.loads(is_up)
            article_obj = models.Article.objects.filter(pk=article_id,).first()
        #   判断当前文章是否为当前用户所写
            if not article_obj.blog.userinfo == request.user:
        #         检验当前用户是否点了赞，判断点赞数据库中是否有点的记录
                is_click = models.UpAnddown.objects.filter(user=request.user,article=article_obj)
                if not is_click:        #用户没有点过
        #             添加数据库，并且对article中普通字段进行同步，
                    #  判断点了赞还是踩，从而加1
                    if is_up:
                        #点赞加1
                        models.Article.objects.filter(pk=article_id).update(up_num=F("up_num")+1)
                        back_dic['msg']="点赞成功"
                    else:
                        #点踩加1
                        models.Article.objects.filter(pk=article_id).update(down_num=F("down_num") + 1)
                        back_dic['msg'] = "点踩成功"

        #            操作点赞点踩表：
                    models.UpAnddown.objects.create(user=request.user,article=article_obj,is_up=is_up)
                    back_dic["msg"]="点赞成功"
                else:
                    back_dic["code"]=201
                    if is_up:
                        back_dic["msg"]:"已经点过赞了"
                    else:
                        back_dic['msg']:'已经点过踩了'
            else:
                back_dic["code"]=202
                back_dic["msg"]="不能为自己的文章点赞哟，快去看看别人的文章吧"
        else:
            back_dic['code']=203
            back_dic['msg']='请先<a href="/login/">登录</a>'

        return JsonResponse(back_dic)

from utils.page import Page
@login_required
def backend(request):
    article_list = models.Article.objects.filter(blog=request.user.blog)
    all_count = article_list.count()
    Page_info = Page(request.GET.get('page'), all_count, 4, 3, '/backend')
    page_queryset = article_list[Page_info.start():Page_info.end()]
    return render(request,"backend/backend.html",locals())

import datetime
from bs4 import BeautifulSoup
@login_required
#添加文章功能
def article_add(request):
    Category_list=models.Category.objects.filter(blog=request.user.blog)
    Tag_list=models.Tag.objects.filter(blog=request.user.blog)
    if request.method == "POST":
        title = request.POST.get("title")
        desc = request.POST.get("desc")
        content = request.POST.get("content")
        category_id = request.POST.get("Category")
        tag_id = request.POST.getlist("Tag")
        # 调用bs4模块对文本内容进行校验，筛选
        soup = BeautifulSoup(content,"html.parser")
        # 找到所有的标签
        obj = soup.find_all()
        for i in obj:
            if i.name==script:  #判断是否为script
                i.decompose()   #将它删除
        article_obj= models.Article.objects.create(
            title=title,
            desc=desc,
            content=str(soup),
            Category_id=category_id,
            # create_time=myNow,
            blog=request.user.blog
        )

    #   操作文章标签表
        article_tag =[]
        for i in tag_id:
            article_tag.append(models.ArticleToTag(article=article_obj,tag_id=i))

        models.ArticleToTag.objects.bulk_create(article_tag)
        return redirect('/backend/')

    return render(request,"backend/article_add.html",locals())

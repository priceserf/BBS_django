from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

# 创建用户表，利用auth_user进行扩展
class UserInfo(AbstractUser):
    phone=models.BigIntegerField(verbose_name="手机号",null=True,blank=True)
    avatar = models.FileField(upload_to="avatar/",default='avatar/default.jpg',verbose_name="默认头像")     #default.png为默认头像的名称
    creat_time = models.DateField(auto_now_add=True)

    # 与个人站点表建立一个一对一的关系
    blog = models.OneToOneField(to='Blog',null=True,on_delete='models.DO_NOTHING')

    def __str__(self):
        return self.username

# 创建个人站点的表数据
class Blog(models.Model):
    site_name = models.CharField(verbose_name="站点名称",max_length=64)
    site_title = models.CharField(verbose_name="站点标题",max_length=32)
    site_theme = models.CharField(verbose_name="站点样式",max_length=64)   #用于存放css/js样式


    def __str__(self):
        return self.site_name

#  创建文章分类表
class Category(models.Model):
    name=models.CharField(verbose_name="文章分类",max_length=32)

#   与个人站点表是一个一对多的关系
    blog = models.ForeignKey(to="Blog",null=True,on_delete="models.CASCADE")

    def __str__(self):
        return self.name

# 创建文章标签表
class Tag(models.Model):
    name = models.CharField(verbose_name="文章标签",max_length=64)

    blog = models.ForeignKey(to="Blog", null=True, on_delete="models.CASCADE")

    def __str__(self):
        return self.name
# 创建文章表
class Article(models.Model):
    title = models.CharField(verbose_name="文章标题",max_length=32)
    desc = models.CharField(verbose_name='文章简介',max_length=128)
    content = models.TextField(verbose_name="文章内容")
    create_time = models.DateTimeField(verbose_name="文章创建时间",null=False)

#   数据库优化
    up_num = models.BigIntegerField(default=0)
    down_num = models.BigIntegerField(default=0)
    comment_name = models.BigIntegerField(verbose_name='评论数',default=0)

#  与个人站点表是一对多的关系
    blog = models.ForeignKey(to="Blog",null=True,on_delete="models.CASCADE")
#  与文章分类表是一对多的关系
    Category = models.ForeignKey(to='Category',null=True,on_delete="models.CASCADE")
#  文章表与标签是多对多的关系，创建第三张表ArticleToTag
    tags = models.ManyToManyField(to='Tag',
                                  through='ArticleToTag',
                                  through_fields=('article','tag')
                                  )

    def __str__(self):
        return self.title


class ArticleToTag(models.Model):
    article = models.ForeignKey(to='Article',on_delete='models.DO_NOTHING')
    tag = models.ForeignKey(to='Tag',on_delete='models.DO_NOTHING')
    #

# 创建点赞表
class UpAnddown(models.Model):
    user = models.ForeignKey(to='UserInfo',verbose_name="点赞用户名",on_delete='models.DO_NOTHING')
    article = models.ForeignKey(to="Article",verbose_name='点赞的文章名',on_delete='models.DO_NOTHING')
    is_up = models.BooleanField()

# 评论表
class Comment(models.Model):
    user = models.ForeignKey(to='UserInfo', verbose_name="点赞用户名",on_delete='models.DO_NOTHING')
    article = models.ForeignKey(to="Article", verbose_name='点赞的文章名',on_delete='models.DO_NOTHING')
    content = models.CharField(verbose_name='评论内容',max_length=128)
    content_time = models.DateTimeField(auto_now_add=True)
#   根评论与子评论
    parent = models.ForeignKey(to='self',null=True,on_delete='models.DO_NOTHING')
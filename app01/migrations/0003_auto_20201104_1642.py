# Generated by Django 3.1.2 on 2020-11-04 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_auto_20201029_2148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='create_time',
            field=models.DateTimeField(null=True, verbose_name='文章创建时间'),
        ),
    ]

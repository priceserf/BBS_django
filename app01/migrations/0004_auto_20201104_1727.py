# Generated by Django 3.1.2 on 2020-11-04 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_auto_20201104_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='create_time',
            field=models.DateTimeField(verbose_name='文章创建时间'),
        ),
    ]

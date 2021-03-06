# Generated by Django 3.0.3 on 2020-02-25 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0004_blogsettings_show_sidebar_toc'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogsettings',
            name='show_sidebar_toc',
        ),
        migrations.AlterField(
            model_name='sidebar',
            name='display_type',
            field=models.PositiveIntegerField(choices=[(1, 'HTML'), (2, '最新文章'), (3, '最热文章'), (4, '最近评论')], default=1, verbose_name='展示类型'),
        ),
    ]

# Generated by Django 3.0.3 on 2020-02-22 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0005_auto_20200222_2311'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogsettings',
            name='index_post_count',
            field=models.PositiveIntegerField(default=8, verbose_name='首页文章展示数目'),
        ),
    ]

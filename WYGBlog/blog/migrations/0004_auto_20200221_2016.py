# Generated by Django 3.0.3 on 2020-02-21 12:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
        ('blog', '0003_auto_20200221_2011'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='blog',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='home.Blog', verbose_name='所属博客'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='blog',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='home.Blog', verbose_name='所属博客'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tag',
            name='blog',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='home.Blog', verbose_name='所属博客'),
            preserve_default=False,
        ),
    ]

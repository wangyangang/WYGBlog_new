# Generated by Django 3.0.3 on 2020-02-24 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='title',
            field=models.CharField(max_length=50, unique=True, verbose_name='标题'),
        ),
        migrations.AlterField(
            model_name='sidebar',
            name='title',
            field=models.CharField(max_length=50, unique=True, verbose_name='标题'),
        ),
        migrations.AlterField(
            model_name='topbar',
            name='name',
            field=models.CharField(default='a', max_length=20, unique=True, verbose_name='名称'),
            preserve_default=False,
        ),
    ]

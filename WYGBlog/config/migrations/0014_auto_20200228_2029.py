# Generated by Django 3.0.3 on 2020-02-28 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0013_auto_20200228_2020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='title',
            field=models.CharField(max_length=50, verbose_name='标题'),
        ),
        migrations.AlterField(
            model_name='topbar',
            name='name',
            field=models.CharField(max_length=20, verbose_name='名称'),
        ),
    ]
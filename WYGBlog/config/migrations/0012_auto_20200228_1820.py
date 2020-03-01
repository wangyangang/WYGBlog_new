# Generated by Django 3.0.3 on 2020-02-28 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0011_auto_20200226_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sidebar',
            name='content',
            field=models.CharField(blank=True, help_text='展示内容(自定义HTML才需要填)', max_length=500, null=True, verbose_name='展示内容(自定义HTML才需要填)'),
        ),
        migrations.AlterField(
            model_name='sidebar',
            name='display_index',
            field=models.PositiveIntegerField(blank=True, default=1, verbose_name='展示顺序(数字大的靠前)'),
        ),
    ]

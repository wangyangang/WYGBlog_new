# Generated by Django 3.0.3 on 2020-02-25 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20200224_2234'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='is_md',
        ),
    ]

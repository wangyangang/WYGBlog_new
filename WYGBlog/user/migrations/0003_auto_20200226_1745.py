# Generated by Django 3.0.3 on 2020-02-26 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20200226_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloguser',
            name='nickname',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='昵称'),
        ),
    ]
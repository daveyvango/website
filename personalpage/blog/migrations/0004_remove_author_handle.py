# Generated by Django 2.1.5 on 2019-01-17 19:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20190117_1947'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='handle',
        ),
    ]

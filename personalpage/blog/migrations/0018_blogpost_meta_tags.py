# Generated by Django 2.1.5 on 2019-03-09 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_blogpost_banner_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='meta_tags',
            field=models.CharField(default='', max_length=200),
        ),
    ]

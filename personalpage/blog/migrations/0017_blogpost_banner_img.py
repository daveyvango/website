# Generated by Django 2.1.5 on 2019-03-08 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_author_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='banner_img',
            field=models.CharField(default='', max_length=100),
        ),
    ]

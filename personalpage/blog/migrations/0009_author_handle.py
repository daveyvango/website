# Generated by Django 2.1.5 on 2019-01-17 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_remove_author_handle'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='handle',
            field=models.CharField(default='na', max_length=20, unique=True),
        ),
    ]
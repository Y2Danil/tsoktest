# Generated by Django 3.0.5 on 2020-07-18 19:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Top', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='like_status',
            field=models.ManyToManyField(blank=True, related_name='user_like', to=settings.AUTH_USER_MODEL),
        ),
    ]
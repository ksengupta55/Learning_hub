# Generated by Django 4.2.6 on 2023-11-28 06:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MediaCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
            ],
            options={
                'verbose_name_plural': 'media categories',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=200, unique=True)),
                ('keywords', models.CharField(blank=True, max_length=200)),
                ('submitted', models.DateTimeField(auto_now_add=True)),
                ('video', models.FileField(null=True, upload_to='video/%y')),
                ('createdby', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('media_category', models.ForeignKey(max_length=50, null=True, on_delete=django.db.models.deletion.CASCADE, to='video.mediacategory')),
            ],
        ),
    ]
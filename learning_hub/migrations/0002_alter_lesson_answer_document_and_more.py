# Generated by Django 4.2.6 on 2023-11-29 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning_hub', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='answer_document',
            field=models.FileField(null=True, upload_to='static/pdf/answer'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='problem_document',
            field=models.FileField(null=True, upload_to='static/pdf'),
        ),
    ]
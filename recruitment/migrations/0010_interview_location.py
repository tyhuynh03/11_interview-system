# Generated by Django 5.1 on 2025-05-10 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruitment', '0009_interview_duration_interview_interview_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='interview',
            name='location',
            field=models.CharField(blank=True, help_text='Địa điểm phỏng vấn', max_length=200, null=True),
        ),
    ]

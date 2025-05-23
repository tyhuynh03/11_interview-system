# Generated by Django 5.1 on 2025-04-22 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruitment', '0005_position_salary_range'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='employment_type',
            field=models.CharField(choices=[('full_time', 'Full-time'), ('part_time', 'Part-time'), ('contract', 'Contract'), ('temporary', 'Temporary'), ('internship', 'Internship'), ('remote', 'Remote')], default='full_time', max_length=20, verbose_name='Employment Type'),
        ),
    ]

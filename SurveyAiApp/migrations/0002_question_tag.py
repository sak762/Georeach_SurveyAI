# Generated by Django 4.2 on 2024-05-08 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SurveyAiApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='tag',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]

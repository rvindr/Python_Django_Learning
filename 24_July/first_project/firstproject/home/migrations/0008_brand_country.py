# Generated by Django 4.2.14 on 2024-07-24 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_alter_skills_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='country',
            field=models.CharField(default='IN', max_length=100),
        ),
    ]

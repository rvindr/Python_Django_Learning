# Generated by Django 4.2.14 on 2024-08-01 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bmp_id', models.CharField(max_length=100, unique=True)),
                ('store_name', models.CharField(max_length=100)),
            ],
        ),
    ]

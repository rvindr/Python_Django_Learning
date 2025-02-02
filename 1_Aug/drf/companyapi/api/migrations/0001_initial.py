# Generated by Django 4.2.14 on 2024-08-01 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('company_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=50)),
                ('about', models.TextField()),
                ('company_type', models.CharField(choices=[('IT', 'IT'), ('NON-IT', 'NON-IT'), ('MOBILES', 'MOBILES')], max_length=100)),
                ('added', models.DateField(auto_now=True)),
                ('active', models.BooleanField(default=False)),
            ],
        ),
    ]

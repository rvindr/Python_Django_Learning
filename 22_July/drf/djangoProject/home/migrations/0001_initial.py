# Generated by Django 4.2.14 on 2024-07-22 08:25

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('created_at', models.DateField(auto_created=True)),
                ('uid', models.UUIDField(default=uuid.UUID('6316470b-10c2-48e0-8d27-1334d7ee8fff'), editable=False, primary_key=True, serialize=False)),
                ('updated_at', models.DateField(auto_now_add=True)),
                ('todo_title', models.CharField(max_length=100)),
                ('todo_description', models.TextField()),
                ('is_done', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

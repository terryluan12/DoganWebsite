# Generated by Django 5.1.2 on 2024-10-30 12:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='admin',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='admin_game', to=settings.AUTH_USER_MODEL),
        ),
    ]
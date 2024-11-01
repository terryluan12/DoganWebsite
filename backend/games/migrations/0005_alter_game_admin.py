# Generated by Django 5.1.2 on 2024-10-31 22:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0004_alter_game_admin'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='admin',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='admin_game', to=settings.AUTH_USER_MODEL),
        ),
    ]

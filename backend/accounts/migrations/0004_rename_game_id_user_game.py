# Generated by Django 5.1.2 on 2024-10-29 19:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_user_email_alter_user_game_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='game_id',
            new_name='game',
        ),
    ]
# Generated by Django 5.1.2 on 2024-10-25 13:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_rename_phone_number_user_phone_alter_user_user_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='phone',
            new_name='phone_number',
        ),
    ]
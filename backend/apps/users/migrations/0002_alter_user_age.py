# Generated by Django 5.1.2 on 2024-11-11 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.IntegerField(blank=True, default=0, editable=False, null=True),
        ),
    ]

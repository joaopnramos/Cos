# Generated by Django 3.0.5 on 2020-08-25 22:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='scientist',
            old_name='is_active',
            new_name='verified',
        ),
    ]
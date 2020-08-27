# Generated by Django 3.0.8 on 2020-08-27 09:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Donator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.IntegerField()),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_donator', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='donator', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Scientist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.PositiveIntegerField(unique=True)),
                ('image', models.ImageField(upload_to='')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('work_local', models.CharField(max_length=100)),
                ('bi', models.PositiveIntegerField(unique=True)),
                ('address', models.CharField(blank=True, max_length=100)),
                ('is_scientist', models.BooleanField(default=True)),
                ('verified', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='scientist', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.IntegerField()),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.CharField(max_length=500)),
                ('periodChoice', models.CharField(choices=[('1', '1 time'), ('2', '2 times'), ('3', '3 times'), ('4', '4 times'), ('5', '5 times')], max_length=2)),
                ('spacetimeChoice', models.CharField(choices=[('30', '30 minutes'), ('1', '1 hour'), ('2', '2 hours'), ('3', '12 hours'), ('24', '1 Day')], max_length=2)),
                ('sensorsChoice', models.CharField(choices=[('a', 'all')], max_length=2)),
                ('finished', models.BooleanField(default=False)),
                ('donator', models.ManyToManyField(blank=True, to='webapp.Donator')),
                ('scientist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scientist', to='webapp.Scientist')),
            ],
        ),
        migrations.CreateModel(
            name='DataGive',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('givingFinished', models.BooleanField(default=False)),
                ('donator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='give_data', to='webapp.Donator')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='give_data', to='webapp.Project')),
            ],
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.CharField(max_length=50)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='data', to='webapp.Project')),
            ],
        ),
    ]

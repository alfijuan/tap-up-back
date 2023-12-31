# Generated by Django 4.2.7 on 2023-11-20 02:44

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
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_id', models.CharField(choices=[('0000', 'Usuario'), ('3003', 'Administrador')], default='0000', max_length=4)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('license', models.SlugField(max_length=1000)),
                ('model', models.CharField(blank=True, default='', max_length=5000)),
                ('year', models.CharField(blank=True, default='', max_length=5000)),
                ('owner', models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, related_name='cars', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.CharField(blank=True, default='', max_length=5000)),
                ('date', models.DateTimeField(null=True)),
                ('comments', models.CharField(blank=True, default='', max_length=5000)),
                ('vehicle', models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, related_name='appointments', to='backend.car')),
            ],
        ),
    ]

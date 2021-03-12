# Generated by Django 3.1 on 1980-01-01 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('email', models.EmailField(max_length=255, verbose_name='email address')),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('profile_pic', models.ImageField(upload_to='user_profile', verbose_name='Profile Picture')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

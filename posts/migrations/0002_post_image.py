# Generated by Django 3.1.3 on 2020-12-12 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(default='This is a picture', upload_to='post_images'),
            preserve_default=False,
        ),
    ]

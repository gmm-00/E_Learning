# Generated by Django 4.2.5 on 2023-09-19 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0008_delete_test_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursemodule',
            name='video',
            field=models.FileField(upload_to='video/%y'),
        ),
    ]

# Generated by Django 2.1.4 on 2019-03-09 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20190309_0318'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='converter',
            name='image',
        ),
        migrations.AddField(
            model_name='converter',
            name='image_file',
            field=models.CharField(max_length=200, null=True),
        ),
    ]

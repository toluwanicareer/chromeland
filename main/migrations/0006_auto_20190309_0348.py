# Generated by Django 2.1.4 on 2019-03-09 14:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20190309_0336'),
    ]

    operations = [
        migrations.RenameField(
            model_name='converter',
            old_name='slug',
            new_name='slug_title',
        ),
    ]
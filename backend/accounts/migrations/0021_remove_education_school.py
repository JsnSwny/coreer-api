# Generated by Django 3.2.18 on 2023-03-31 00:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_auto_20230330_1456'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='education',
            name='school',
        ),
    ]

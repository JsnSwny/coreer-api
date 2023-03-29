# Generated by Django 3.2.18 on 2023-03-29 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_education_project_university'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='University',
            new_name='School',
        ),
        migrations.RemoveField(
            model_name='education',
            name='university',
        ),
        migrations.AddField(
            model_name='education',
            name='school',
            field=models.ManyToManyField(to='accounts.School'),
        ),
    ]

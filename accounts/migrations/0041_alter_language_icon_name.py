# Generated by Django 4.2.2 on 2023-06-12 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0040_alter_customuser_bio"),
    ]

    operations = [
        migrations.AlterField(
            model_name="language",
            name="icon_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

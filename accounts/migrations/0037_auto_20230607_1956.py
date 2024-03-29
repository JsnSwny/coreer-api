# Generated by Django 3.2.19 on 2023-06-07 18:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0036_careerlevel_careerpreferences'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='current_level',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='current_level_users', to='accounts.careerlevel'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='looking_for',
            field=models.ManyToManyField(related_name='looking_for_users', to='accounts.CareerLevel'),
        ),
        migrations.DeleteModel(
            name='CareerPreferences',
        ),
    ]

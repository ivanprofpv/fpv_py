# Generated by Django 4.2.4 on 2023-09-29 10:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drone', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='drone',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='drone.drone'),
        ),
    ]
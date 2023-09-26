# Generated by Django 4.2.5 on 2023-09-26 17:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drone', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComponentCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Категории компонентов',
                'verbose_name_plural': 'Категории компонентов',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, db_index=True, max_length=255, verbose_name='Название')),
                ('url', models.CharField(blank=True, max_length=255, verbose_name='Ссылка')),
                ('price', models.IntegerField(blank=True, verbose_name='Цена')),
                ('component_category_key', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='drone.componentcategory')),
                ('drone_key', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='drone.drone')),
            ],
        ),
    ]

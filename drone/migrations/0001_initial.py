# Generated by Django 4.2.4 on 2023-09-28 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200, verbose_name='Название')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Категории',
                'verbose_name_plural': 'Категории',
                'ordering': ['id'],
            },
        ),
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
            name='Drone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('content', models.TextField(verbose_name='Текст статьи')),
                ('drone_photo', models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='Фото')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Время обновления')),
                ('is_published', models.BooleanField(default=True, verbose_name='Публикация')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='drone.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Дроны',
                'verbose_name_plural': 'Дроны',
                'ordering': ['-time_create', 'title'],
            },
        ),
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, db_index=True, max_length=100, verbose_name='Название')),
                ('url', models.CharField(blank=True, max_length=255, verbose_name='Ссылка')),
                ('price', models.IntegerField(blank=True, verbose_name='Цена')),
                ('component_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='drone.componentcategory')),
                ('drone', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='drone.drone')),
            ],
        ),
    ]

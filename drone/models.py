from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import slugify as django_slugify
from django.urls import reverse
from PIL import Image

User=get_user_model()

alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
            'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e', 'ю': 'yu',
            'я': 'ya'}

def slugify(s):
    """
    Overriding django slugify that allows to use russian words as well.
    """
    return django_slugify(''.join(alphabet.get(w, w) for w in s.lower()))
class Drone(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    content = models.TextField(blank=False, verbose_name='Текст статьи')
    drone_photo = models.ImageField(upload_to="photos/%Y/%m/%d", verbose_name='Фото')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    is_published = models.BooleanField(default=True, verbose_name='Публикация')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, verbose_name='Категория')
    likes = models.ManyToManyField(User, related_name='drone_like')

    def __str__(self):
        return self.title

    # формирует маршрут к конкретной записи
    def get_absolute_url(self):
        return reverse('drone', kwargs={'drone_slug': self.slug})

    #добавляем "-id" в конце url для уникальности
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        if not self.slug.endswith('-' + str(self.pk)):
            self.slug += '-' + str(self.pk)
        super().save(*args, **kwargs)

    def count_of_likes(self):
        return self.likes.count()

    class Meta:
        verbose_name = 'Дроны'
        verbose_name_plural = 'Дроны'
        ordering = ['-time_create', 'title']

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'
        ordering = ['id']

class ComponentCategory(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('component_category', kwargs={'component_category_slug': self.slug})

    class Meta:
        verbose_name = 'Категории компонентов'
        verbose_name_plural = 'Категории компонентов'
        ordering = ['id']

class Component(models.Model):
    name = models.CharField(max_length=100, db_index=True, blank=True, verbose_name='Название')
    url = models.CharField(max_length=255, blank=True, verbose_name='Ссылка')
    price = models.IntegerField(blank=True, verbose_name='Цена')
    drone = models.ForeignKey('Drone', on_delete=models.PROTECT, null=True)
    component_category = models.ForeignKey('ComponentCategory', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name

class Comment(models.Model):
    content = models.CharField(max_length=255, verbose_name='Комментарий')
    created_on = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False, verbose_name='Публикация')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    drone = models.ForeignKey(Drone, on_delete=models.CASCADE, related_name='comments', null=False)

    def __str__(self):
        return 'Комментарий: {} от: {}, пост: {}'.format(self.content, self.author, self.drone)

    class Meta:
        verbose_name = 'Комментарии'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_on']

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(blank=True)
    avatar = models.ImageField(default='profile_images/default.jpg', upload_to='profile_images', verbose_name='Аватар', blank=True)
    bio = models.TextField(max_length=255, blank=True, verbose_name='О себе')

    def __str__(self):
        return self.user.username

    # ресайз аватарок
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 250 or img.width > 250:
            new_img = (250, 250)
            img.thumbnail(new_img)
            img.save(self.avatar.path)
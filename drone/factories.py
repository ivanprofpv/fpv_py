import factory
from django.contrib.auth.models import User
from .models import *

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'password')

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

name = factory.Sequence(lambda n: f'Category test{n}')
slug = factory.Sequence(lambda n: f'category-test{n}')


class DroneFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Drone

    author = factory.SubFactory(UserFactory) # Связываем автора с юзером
    title = factory.Sequence(lambda n: f'Drone test{n}')
    slug = factory.Sequence(lambda n: f'drone-test{n}')
    content = factory.Faker('text')
    drone_photo = factory.django.ImageField(filename='drone/img/default.jpg')
    is_published = True
    category = factory.SubFactory(CategoryFactory)

class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    content = factory.Sequence(lambda n: f'Drone test comment{n}')
    author = factory.SubFactory(UserFactory) # Связываем автора с юзером
    drone = factory.SubFactory(DroneFactory) # Связываем коммент с дроном




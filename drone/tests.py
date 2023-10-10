from django.forms import inlineformset_factory
from django.test import TestCase
from .factories import *
from .forms import AddComponentForm


class DroneHomeTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = UserFactory.create() # Создаем юзера с помощью фабрики

        category = CategoryFactory.create()

        DroneFactory.create(author=test_user, category=category)
        DroneFactory.create(author=test_user, category=category)
        DroneFactory.create(author=test_user, category=category, is_published=False)

    def test_view_url_home_exists(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)

    def test_view_use_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'drone/index.html')

    # Проверяем, что на главной только 2 опубликованных поста
    def test_views_returns_only_published_drone(self):
        response = self.client.get(reverse('home'))
        drones = response.context['post']
        self.assertEqual(drones.count(), 2)

    def test_views_context_contains_title(self):
        response = self.client.get(reverse('home'))
        title = response.context['title']
        self.assertEqual(title, 'Главная страница')

class CreatePostTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory.create()

    # GET-запрос, проверяем, что страница есть для авторизованного юзера
    def test_get_context_data_auth_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('add_drone'))
        self.assertEquals(response.status_code, 200)

    def test_get_context_data_not_auth_user(self):
        response = self.client.get(reverse('add_drone'))
        self.assertEquals(response.status_code, 302)

from django.db import models
from django.urls import reverse


class Drone(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=False)
    drone_photo = models.ImageField(upload_to="photos/%Y/%m/%d")
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    # формирует маршрут к конкретной записи
    def get_absolute_url(self):
        return reverse('drone', kwargs={'drone_id': self.pk})

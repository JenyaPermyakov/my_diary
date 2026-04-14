from django.db import models
from django.utils import timezone

class Entry(models.Model):

    STATUS_CHOICES = [
        ("new", "Новая"),
        ("progress", "В процессе"),
        ("done", "Завершена"),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    time_limit = models.DateTimeField(default=0)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default = "new",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Entries'


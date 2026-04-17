from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class Entry(models.Model):

    STATUS_CHOICES = [
        ("new", "Новая"),
        ("progress", "В процессе"),
        ("done", "Завершена"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    time_limit = models.DateTimeField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default = "new",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Entries'


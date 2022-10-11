from django.conf import settings
from django.db import models
from django.utils import timezone


class AdvertisementStatusChoices(models.TextChoices):
    """Статусы объявления."""

    OPEN = "OPEN", "Открыто"
    CLOSED = "CLOSED", "Закрыто"
    DRAFT = "DRAFT", "Черновик"


class Advertisement(models.Model):
    """Объявление."""

    title = models.TextField()
    description = models.TextField(default='')
    status = models.TextField(
        choices=AdvertisementStatusChoices.choices,
        default=AdvertisementStatusChoices.DRAFT
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='creators',
    )
    created_at = models.DateTimeField(
        default=timezone.now
        # auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    favorite = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorites',
        null=True,
        # limit_choices_to={'favorites': creator }
    )

    def __str__(self):
        return f'{self.title} // {self.description}'

from typing import Any, Iterable
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone


class User(AbstractUser):
    first_name = models.TextField(
        verbose_name="Имя пользователя",
        null=False,
        blank=False,
    )
    last_name = models.TextField(
        verbose_name="Фамилия пользователя",
        null=True,
        blank=True,
    )
    phone = models.TextField(
        verbose_name="Номер телефона",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self) -> str:
        return self.username


class Pet(models.Model):
    BREED_CHOICES = [
        ("LAB", "Labrador"),
        ("BEA", "Beagle"),
        ("PUG", "Pug"),
        ("POM", "Pomeranian"),
        ("OTH", "Other"),
    ]

    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=3, choices=BREED_CHOICES, default="OTH")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pets")

    class Meta:
        verbose_name = "Питомец"
        verbose_name_plural = "Питомцы"

    def __str__(self) -> str:
        return self.name


class Walker(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Исполнитель"
        verbose_name_plural = "Исполнители"

    def __str__(self) -> str:
        return self.name


class WalkOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="walk_orders")
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="walk_orders")
    walker = models.ForeignKey(Walker, on_delete=models.CASCADE, related_name="walk_orders")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    comment = models.TextField()

    def clean(self) -> None:
        if self.start_time.minute not in [0, 30]:
            raise ValidationError(
                "Прогулки должны начинаться в начале часа или в середине часа."
            )

        if self.end_time > self.start_time + timezone.timedelta(minutes=30):
            raise ValidationError(
                "Прогулка не может длиться болтше чем через 30 минут."
            )

        if self.start_time < 7 or self.start_time > 23:
            raise ValidationError(
                "Прогулки не могут начинаться раньше 7 утра или после 11 вечера."
            )

        if WalkOrder.objects.filter(
            start_time=self.start_time, walker=self.walker
        ).exists():
            raise ValidationError(
                f"{self.walker.name} на это время уже назначена прогулка."
            )

    def save(self, *args: tuple, **kwargs: dict[str, Any]) -> None:
        self.clean()
        self.end_time = self.start_time + timezone.timedelta(minutes=30)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.user.username} - {self.pet.name} - {self.walker.name} - {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

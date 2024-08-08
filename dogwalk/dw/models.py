from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractUser
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

    name = models.CharField(max_length=100, verbose_name="Кличка животного")
    breed = models.CharField(
        max_length=3, choices=BREED_CHOICES, default="OTH", verbose_name="Порода"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="pets",
        verbose_name="Хозяин животного",
    )

    class Meta:
        verbose_name = "Питомец"
        verbose_name_plural = "Питомцы"

    def __str__(self) -> str:
        return self.name


class Walker(models.Model):
    name_walker = [
        ("Peter", "Peter"),
        ("Anton", "Anton"),
    ]
    name = models.CharField(
        max_length=5,
        choices=name_walker,
        default="Peter",
        verbose_name="Имя исполнителя",
    )

    class Meta:
        verbose_name = "Исполнитель"
        verbose_name_plural = "Исполнители"

    def __str__(self) -> str:
        return self.name


class WalkOrder(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="walk_orders",
        verbose_name="Заказчик",
    )
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name="walk_orders",
        verbose_name="Кличка животного",
    )
    walker = models.ForeignKey(
        Walker,
        on_delete=models.CASCADE,
        related_name="walk_orders",
        verbose_name="Исполнитель",
    )
    start_time = models.DateTimeField(verbose_name="Время начала прогулки")
    end_time = models.DateTimeField(verbose_name="Время окончания прогулки")
    comment = models.TextField(verbose_name="Комментарий")

    def save(self, *args: tuple, **kwargs: dict[str, Any]) -> None:
        self.clean()
        self.end_time = self.start_time + timezone.timedelta(minutes=30)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.user.username} - {self.pet.name} - {self.walker.name} - {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

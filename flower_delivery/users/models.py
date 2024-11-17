# users/models.py
from django.contrib.auth.models import User
from django.db import IntegrityError, models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Адрес доставки")
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="Номер телефона")
    email = models.EmailField(max_length=255, blank=True, null=True,  verbose_name="Адрес электронной почты")
    telegram_id = models.BigIntegerField(unique=True, blank=True, null=True, verbose_name="Telegram ID")  # Новое поле

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        if self.telegram_id:
            # Проверка на существующий `telegram_id`
            if Profile.objects.filter(telegram_id=self.telegram_id).exclude(id=self.id).exists():
                raise IntegrityError(f"Этот Telegram ID уже привязан к другому профилю.")
        super().save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


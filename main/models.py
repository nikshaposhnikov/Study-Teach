from django.dispatch import Signal
from django.db import models
from django.contrib.auth.models import AbstractUser

from .utilities import send_activation_notification, get_timestamp_path

class AdditionalImage(models.Model):
    bb = models.ForeignKey('Bb', on_delete=models.CASCADE, verbose_name='Объявление')
    image = models.ImageField(upload_to=get_timestamp_path, verbose_name='Изображение')

    class Meta:
        verbose_name_plural = 'Дополнительные иллюстрации'
        verbose_name = 'Дополнительная иллюстрация'

class Bb(models.Model):
    group = models.ForeignKey('SubGroup', on_delete=models.PROTECT, verbose_name='Группа')
    title = models.CharField(max_length=40, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Информация')
    image = models.ImageField(blank=True, upload_to=get_timestamp_path, verbose_name='Изображение')
    author = models.ForeignKey('AdvUser', on_delete=models.CASCADE,
                               verbose_name='Автор объявления')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Выводить в списке?')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')

    def __str__(self):
        return self.group.name

    def delete(self, *args, **kwargs):
        for ai in self.additionalimage_set.all():
            ai.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Объявления'
        verbose_name = 'Объявление'
        ordering = ['-created_at']

class Group(models.Model):
    name = models.CharField(max_length=20, db_index=True, unique=True, verbose_name='Название')
    order = models.SmallIntegerField(default=0, db_index=True, verbose_name='Порядок')
    super_group = models.ForeignKey('SuperGroup', on_delete=models.PROTECT, null=True, blank=True,
                                     verbose_name='Форма обучения')

class SuperGroupManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_group__isnull=True)

class SuperGroup(Group):
    objects = SuperGroupManager()

    def __str__(self):
        return self.name

    class Meta:
        proxy = True
        ordering = ["order", "name"]
        verbose_name = 'Форма обучения'
        verbose_name_plural = 'Формы обучения'

class SubGroupManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_group__isnull=False)

class SubGroup(Group):
    objects = SubGroupManager()

    def __str__(self):
        return '%s - %s' % (self.super_group.name, self.name)

    class Meta:
        proxy = True
        ordering = ['super_group__order', 'super_group__name', 'order', 'name']
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

user_registrated = Signal(providing_args=['instance'])

def user_registrated_dispatcher(sender, **kwargs):
    send_activation_notification(kwargs['instance'])

user_registrated.connect(user_registrated_dispatcher)

class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Прошел активацию?')
    send_messages = models.BooleanField(default=True, verbose_name='Слать оповещания о новых комментариях?')

    def delete(self, *args, **kwargs):
        for bb in self.bb_set.all():
            bb.delete()
        super().delete(*args, **kwargs)

    class Meta(AbstractUser.Meta):
        pass


from django.db import models

class Bb(models.Model):
     title = models.CharField(max_length=50, verbose_name='Заголовок')
     content = models.TextField(null=True, verbose_name='Описание')
     published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
     group = models.ForeignKey('Group', null=True, on_delete=models.PROTECT, verbose_name='Группа')

     class Meta:
         verbose_name_plural = 'Объявления'
         verbose_name = 'Объявление'
         ordering = ['-published']

class Group(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Группы'
        verbose_name = 'Группа'
        ordering = ['-name']




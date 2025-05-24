from django.db import models


class City(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Населенный пункт'
        verbose_name_plural = 'Населенные пункты'

    def __str__(self):
        return self.name

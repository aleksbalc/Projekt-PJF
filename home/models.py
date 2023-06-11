from django.forms import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class ZadaniaStale(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    def str(self):
        return self.name


class PrzydzieloneZadanieStale(models.Model):
    id_zs = models.ForeignKey(ZadaniaStale, on_delete=models.CASCADE, default=1, related_name='assigned_tasks')
    host = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='hosted_tasks')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='received_tasks')
    created = models.DateTimeField(default=timezone.now)
    started = models.DateTimeField(null=True, blank=True)
    finished = models.DateTimeField(null=True, blank=True)


class ZadaniaJednorazowe(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)
    started = models.DateTimeField(null=True, blank=True)
    finished = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created']

    def str(self):
        return self.name


class H_ZadaniaStale(models.Model):
    id_pzs = models.ForeignKey(PrzydzieloneZadanieStale, on_delete=models.CASCADE, default=1)
    started = models.DateTimeField(null=True, blank=True)
    finished = models.DateTimeField(null=True, blank=True)


class H_ZadaniaJednorazowe(models.Model):
    id_pzs = models.ForeignKey(ZadaniaJednorazowe, on_delete=models.CASCADE, default=1)
    started = models.DateTimeField(null=True, blank=True)
    finished = models.DateTimeField(null=True, blank=True)
from django.forms import ValidationError
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

class PracownikManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(email='pracownik@mail.com')

class ZadaniaStale(models.Model):

    PROGRESS_CHOICES = (
        ('przydzielone', 'Przydzielone'),
        ('rozpoczęte', 'Rozpoczęte'),
        ('zakończone', 'Zakończone'),
    )

    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hosted_tasks', default=1)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    recipients = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_tasks', limit_choices_to={'email': 'pracownik@mail.com'})
    progress = models.CharField(max_length=20, choices=PROGRESS_CHOICES, null=True, default='przydzielone')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(default=timezone.now)

    objects = models.Manager()
    pracownik_objects = PracownikManager()

    def clean(self):
        if self.recipients is None:
            raise ValidationError("At least one recipient must be selected.")

    def __str__(self):
        return self.name
    
class ZadaniaJednorazowe(models.Model):

    PROGRESS_CHOICES = (
        ('rozpoczęte', 'Rozpoczęte'),
        ('zakończone', 'Zakończone'),
    )

    host = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    progress = models.CharField(max_length=20, choices=PROGRESS_CHOICES, default='rozpoczęte')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name




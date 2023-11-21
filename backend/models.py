from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

date_format = '%Y-%m-%dT%H:%M:%S.%fZ'

class Car(models.Model):
    license = models.SlugField(max_length=1000)
    model = models.CharField(max_length=5000, default='', blank=True)
    year = models.CharField(max_length=5000, default='', blank=True)
    owner = models.ForeignKey(User, related_name='cars', on_delete=models.PROTECT, default='')

    def to_json(self):
        return {
            'id': self.id,
            'license': self.license,
            'model': self.model,
            'year': self.year,
            'owner': self.owner.profile.to_json()
        }
    
class Appointment(models.Model):
    vehicle = models.ForeignKey(Car, related_name='appointments', on_delete=models.PROTECT, default='')
    score = models.CharField(max_length=5000, default='', blank=True)
    date = models.DateTimeField(auto_now_add=False, null=True)
    comments = models.CharField(max_length=5000, default='', blank=True)

    def to_json(self):
        return {
            'id': self.id,
            'vehicle': self.vehicle.license,
            'score': self.score if self.score else '-',
            'date': self.date.strftime(date_format) if self.date else '',
            'comments': self.comments,
        }


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type_id = models.CharField(max_length=4, choices=settings.USER_CHOICES, default=settings.USER_CHOICES[0][0])

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def to_json(self):
        return {
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'username': self.user.username,
            'email': self.user.email,
            'type_id': self.type_id,
        }
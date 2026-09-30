from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from secrets import token_urlsafe
from .models import Company


@receiver(post_save, sender=User)
def create_company_for_new_user(sender, instance, created, **kwargs):
    if created:
        Company.objects.create(
            user=instance,
            company_name=instance.username,
            api_key=token_urlsafe(32)
        )
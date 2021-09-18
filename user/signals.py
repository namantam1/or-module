from django.db.models.signals import post_save
from django.dispatch import receiver

from django.utils import timezone

from .models import StudentRegistration


def generate_application_id(id):
    return "MT" + str(timezone.localtime().year) + "{0:04d}".format(id)


@receiver(post_save, sender=StudentRegistration)
def created_myuser(sender, instance=None, created=False, **kwargs):
    if created:
        print("post save created")
        instance.application_id = generate_application_id(instance.id)
        instance.save()

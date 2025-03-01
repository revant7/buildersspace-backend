from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import (
    Participant,
    GryffindorParticipant,
    HufflepuffParticipant,
    RavenclawParticipant,
    SlytherinParticipant,
    PhoenixParticipant,
)


@receiver(post_save, sender=Participant)
def create_house_participant(sender, instance, created, **kwargs):
    if created:
        if instance.house == "Gryffindor":
            GryffindorParticipant.objects.create(participant=instance)
        elif instance.house == "Hufflepuff":
            HufflepuffParticipant.objects.create(participant=instance)
        elif instance.house == "Ravenclaw":
            RavenclawParticipant.objects.create(participant=instance)
        elif instance.house == "Slytherin":
            SlytherinParticipant.objects.create(participant=instance)
        elif instance.house == "Phoenix":
            PhoenixParticipant.objects.create(participant=instance)


@receiver(post_save, sender=Participant)
def update_house_participant(sender, instance, created, **kwargs):
    if not created:
        try:
            if instance.house == "Gryffindor":
                GryffindorParticipant.objects.update_or_create(participant=instance)
            elif instance.house == "Hufflepuff":
                HufflepuffParticipant.objects.update_or_create(participant=instance)
            elif instance.house == "Ravenclaw":
                RavenclawParticipant.objects.update_or_create(participant=instance)
            elif instance.house == "Slytherin":
                SlytherinParticipant.objects.update_or_create(participant=instance)
            elif instance.house == "Phoenix":
                PhoenixParticipant.objects.update_or_create(participant=instance)
        except:
            if instance.house == "Gryffindor":
                GryffindorParticipant.objects.create(participant=instance)
            elif instance.house == "Hufflepuff":
                HufflepuffParticipant.objects.create(participant=instance)
            elif instance.house == "Ravenclaw":
                RavenclawParticipant.objects.create(participant=instance)
            elif instance.house == "Slytherin":
                SlytherinParticipant.objects.create(participant=instance)
            elif instance.house == "Phoenix":
                PhoenixParticipant.objects.create(participant=instance)

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import (
    User,
    Participant,
    Attendee,
    Project,
    VoteCount,
    LikeCount,
    Vote,
    Like,
    SocialLinks,
    ParticipantNotification,
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


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    """
    Handles updates to Participant and Attendee models based on is_participant and is_attendee flags.
    """
    if not created:  # Only run for when there's an update
        if instance.is_participant:
            if not Participant.objects.filter(user=instance).exists():
                participant = Participant(user=instance)
                participant.save()

                Project.objects.create(participant=participant)
                project = Project.objects.get(participant=participant)
                VoteCount(project=project).save()
                LikeCount(project=project).save()
                SocialLinks(user=instance).save()
                ParticipantNotification(participant=participant).save()
        else:
            Participant.objects.filter(user=instance).delete()

        if instance.is_attendee:
            if not Attendee.objects.filter(user=instance).exists():
                Attendee(user=instance).save()
        else:
            Attendee.objects.filter(user=instance).delete()

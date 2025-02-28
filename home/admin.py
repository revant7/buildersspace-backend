from django.contrib import admin
from .models import (
    User,
    Participant,
    Attendee,
    Project,
    GryffindorParticipant,
    HufflepuffParticipant,
    RavenclawParticipant,
    SlytherinParticipant,
    PhoenixParticipant,
    Vote,
    Like,
    VoteCount,
    LikeCount,
    SocialLinks,
    ParticipantNotification,
)

# Register your models here.

admin.site.register(User)
admin.site.register(Participant)
admin.site.register(Attendee)
admin.site.register(Project)
admin.site.register(GryffindorParticipant)
admin.site.register(HufflepuffParticipant)
admin.site.register(RavenclawParticipant)
admin.site.register(SlytherinParticipant)
admin.site.register(PhoenixParticipant)
admin.site.register(Vote)
admin.site.register(Like)
admin.site.register(VoteCount)
admin.site.register(LikeCount)
admin.site.register(SocialLinks)
admin.site.register(ParticipantNotification)

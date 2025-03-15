from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Admin,
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
    UserLoginAttempt,
    UserLoginHistory,
)

# Register your models here.


class CustomAdmin(UserAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
    )
    fieldsets = (
        ("Login Credentials", {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important Dates", {"fields": ("last_login",)}),
    )
    ordering = ("email",)


admin.site.register(Admin, CustomAdmin)
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
admin.site.register(UserLoginAttempt)
admin.site.register(UserLoginHistory)

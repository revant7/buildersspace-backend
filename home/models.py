from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils import timezone
from datetime import timedelta

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            raise ValueError("The Password field must be set.")
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(primary_key=True)
    first_name = models.CharField(max_length=256, null=False, blank=False)
    last_name = models.CharField(max_length=256, null=True, blank=True)
    mobile_number = models.CharField(
        max_length=15, unique=True, null=False, blank=False
    )
    is_participant = models.BooleanField(default=False)
    is_attendee = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "mobile_number"]

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} - {self.email}"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class Participant(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="participant_profile",
        primary_key=True,
    )

    OPTION_CHOICES = [
        ("Gryffindor", "Gryffindor"),
        ("Hufflepuff", "Hufflepuff"),
        ("Ravenclaw", "Ravenclaw"),
        ("Slytherin", "Slytherin"),
        ("Phoenix", "Phoenix"),
    ]

    house = models.CharField(max_length=32, choices=OPTION_CHOICES)

    profile_picture = models.ImageField(
        upload_to="participant/profile/",
        blank=True,
        null=True,
        default="default/Profile.png",
    )

    def __str__(self):
        return f"Participant: {self.user.first_name} - {self.user.email}"

    class Meta:
        verbose_name = "Participant"
        verbose_name_plural = "Participants"


class Attendee(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="attendee_profile",
        primary_key=True,
    )

    def __str__(self):
        return f"Attendee - {self.user.first_name}"


class Project(models.Model):
    participant = models.OneToOneField(
        Participant,
        on_delete=models.CASCADE,
        related_name="participant_project",
        primary_key=True,
    )
    project_idea_title = models.TextField(blank=True, null=True)
    project_idea_description = models.TextField(blank=True, null=True)
    project_experience = models.TextField(blank=True, null=True)
    project_video_link = models.URLField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.participant.user.first_name} - {self.project_idea_title}"

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"


class Vote(models.Model):
    attendee = models.ForeignKey(
        Attendee, on_delete=models.CASCADE, related_name="attendees"
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="project_votes"
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("attendee", "project")

    def __str__(self):
        return f"Participant => {self.project.participant.user.first_name} Vote Given By => {self.attendee.user.first_name}"


class Like(models.Model):
    participant = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE,
        related_name="participant_like",
        null=True,
        blank=True,
    )
    attendee = models.ForeignKey(
        Attendee,
        on_delete=models.CASCADE,
        related_name="attendee_like",
        null=True,
        blank=True,
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="project_likes"
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.participant:
            return f"{self.participant.user.first_name} likes {self.project.project_idea_title}"
        elif self.attendee:
            return f"{self.attendee.user.first_name} likes {self.project.project_idea_title}"
        return f"Unknown user likes {self.project.project_idea_title}"

    class Meta:
        verbose_name = "Like"
        verbose_name_plural = "Likes"


class VoteCount(models.Model):
    project = models.OneToOneField(
        Project, on_delete=models.CASCADE, related_name="vote_count"
    )
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.project.participant.user.first_name} - Votes: {self.count}"

    class Meta:
        verbose_name = "Vote Count"
        verbose_name_plural = "Vote Counts"


class LikeCount(models.Model):
    project = models.OneToOneField(
        Project, on_delete=models.CASCADE, related_name="like_count"
    )
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.project.participant.user.first_name} - Likes: {self.count}"

    class Meta:
        verbose_name = "Like Count"
        verbose_name_plural = "Like Counts"


class SocialLinks(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="social_links"
    )
    instagram = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.user.first_name


class ParticipantNotification(models.Model):
    participant = models.ForeignKey(
        Participant, on_delete=models.CASCADE, related_name="user_notifications"
    )
    notification_title = models.CharField(max_length=256, null=True, blank=True)
    notification_message = models.TextField(default="")
    timestamp = models.DateTimeField(auto_now_add=True)
    house = models.CharField(
        max_length=32, choices=Participant.OPTION_CHOICES, null=True, blank=True
    )
    is_read = models.BooleanField(default=False)

    def __str__(self):
        if self.recipient:
            return f"Notification to {self.recipient.user.first_name}: {self.message[:50]}..."
        elif self.house:
            return f"Notification to {self.house} house: {self.message[:50]}..."
        else:
            return f"Notification to all: {self.message[:50]}..."

    class Meta:
        ordering = ["-timestamp"]  # Show latest notifications first


# Types of participants


class GryffindorParticipant(models.Model):
    participant = models.OneToOneField(
        Participant, on_delete=models.CASCADE, primary_key=True
    )

    def __str__(self):
        return self.participant.name

    class Meta:
        verbose_name = "Gryffindor Participant"
        verbose_name_plural = "Gryffindor Participants"


class HufflepuffParticipant(models.Model):
    participant = models.OneToOneField(
        Participant, on_delete=models.CASCADE, primary_key=True
    )

    def __str__(self):
        return self.participant.name

    class Meta:
        verbose_name = "Hufflepuff Participant"
        verbose_name_plural = "Hufflepuff Participants"


class RavenclawParticipant(models.Model):
    participant = models.OneToOneField(
        Participant, on_delete=models.CASCADE, primary_key=True
    )

    def __str__(self):
        return self.participant.name

    class Meta:
        verbose_name = "Ravenclaw Participant"
        verbose_name_plural = "Ravenclaw Participants"


class SlytherinParticipant(models.Model):
    participant = models.OneToOneField(
        Participant, on_delete=models.CASCADE, primary_key=True
    )

    def __str__(self):
        return self.participant.name

    class Meta:
        verbose_name = "Slytherin Participant"
        verbose_name_plural = "Slytherin Participants"


class PhoenixParticipant(models.Model):
    participant = models.OneToOneField(
        Participant, on_delete=models.CASCADE, primary_key=True
    )

    def __str__(self):
        return self.participant.name

    class Meta:
        verbose_name = "Phoenix Participant"
        verbose_name_plural = "Phoenix Participants"

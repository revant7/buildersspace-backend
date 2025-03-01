from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from . import models

# Create your views here.

# User registration view

User = get_user_model()


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def register_user(request):
    email = request.data.get("email")
    password = request.data.get("password")
    first_name = request.data.get("first_name")
    last_name = request.data.get("last_name", "")
    mobile_number = request.data.get("mobile_number")
    is_participant = request.data.get("is_participant", False)
    is_attendee = request.data.get("is_attendee", False)

    if not email or not password or not first_name or not mobile_number:
        return JsonResponse(
            {
                "error": "All fields (email, password, first_name, mobile_number) are required."
            },
            status=400,
        )

    if User.objects.filter(email=email).exists():
        return JsonResponse(
            {"error": "A user with this email already exists."}, status=400
        )

    user = User.objects.create_user(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        mobile_number=mobile_number,
        is_participant=is_participant,
        is_attendee=is_attendee,
    )

    if user.is_participant:
        participant_house = request.data.get("house")
        profile_picture = request.FILES.get("profile_picture")
        participant = models.Participant(
            user=user, house=participant_house, profile_picture=profile_picture
        )
        participant.save()

        project_idea_title = request.data.get("project_idea_title")
        project_idea_description = request.data.get("project_idea_description")
        project_experience = request.data.get("project_experience")
        project_video_link = request.data.get("project_video_link")
        project = models.Project(
            participant=participant,
            project_idea_title=project_idea_title,
            project_idea_description=project_idea_description,
            project_experience=project_experience,
            project_video_link=project_video_link,
        )
        project.save()

        models.VoteCount(project=project).save()
        models.LikeCount(project=project).save()
        models.SocialLinks(user=user).save()
        models.ParticipantNotification(participant=participant).save()

    return JsonResponse(
        {
            "message": "User registered successfully.",
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "mobile_number": user.mobile_number,
        },
        status=201,
    )


# user login view


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def custom_token_obtain_view(request):
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return JsonResponse(
            {"error": "Both email and password are required."}, status=400
        )

    user = authenticate(email=email, password=password)

    if not user:
        return JsonResponse({"error": "Invalid email or password."}, status=401)

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    return JsonResponse(
        {
            "refresh": str(refresh),
            "access": access_token,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_attendee": user.is_attendee,
            "is_participant": user.is_participant,
            "is_staff": user.is_staff,
        }
    )


def cast_vote(request):
    user = request.user
    if user.is_attendee:
        participant = request.participant
        project = participant.project
        vote = models.Vote.objects.create(attendee=user.attendee, project=project)
        vote_count, created = models.VoteCount.objects.get_or_create(
            project=project, defaults={"count": 0}
        )
        vote_count.count += 1
        vote_count.save()


def do_like(request):
    user = request.user
    project = request.project
    if user.is_attendee:
        like = models.Like.objects.create(attendee=user.attendee, project=project)
        like_count = models.LikeCount.objects.get_or_create(
            project=project, defaults={"count": 0}
        )
        like_count.save()
        like_count.count += 1

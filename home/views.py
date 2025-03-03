from django.shortcuts import render
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from . import models, utils
from .permissions import IsTokenAuthenticated


# Create your views here.


# User registration view
User = models.User


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def register_user(request):
    email = request.data.get("email")
    password = utils.generate_random_password()
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
        models.SocialLinks(
            user=user,
            instagram=request.data.get("instagram"),
            github=request.data.get("github"),
            twitter=request.data.get("twitter"),
            linkedin=request.data.get("linkedin"),
        ).save()
        models.ParticipantNotification(
            participant=participant,
            notification_title=request.data.get("notification_title"),
            notification_message=request.data.get("notification_message"),
            house=request.data.get("house"),
            is_read=request.data.get("is_read"),
        ).save()

    if user.is_attendee:
        attendee = models.Attendee(user=user)
        attendee.save()

    return JsonResponse(
        {
            "message": "User registered successfully.",
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "password": password,
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
        }
    )


# cast the vote


def cast_vote(request):
    user = request.user
    if user.is_attendee:
        participant = request.participant
        project = participant.project
        attendee = user.attendee
        already_voted = models.Vote.get(attendee=attendee)
        if already_voted:
            return JsonResponse({"status": "User Already Voted."})
        vote = models.Vote.objects.create(attendee=user.attendee, project=project)
        vote.save()
        vote_count = models.VoteCount.objects.get(project=project)
        vote_count.count += 1
        vote_count.save()


# post like


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


# patch user data


@api_view(["PATCH"])
@permission_classes([IsTokenAuthenticated])
def update_user(request):
    try:
        user = models.User.objects.get(email=request.user.email)
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    first_name = request.data.get("first_name")
    last_name = request.data.get("last_name")
    mobile_number = request.data.get("mobile_number")
    password = request.data.get("password")

    if first_name is not None:
        user.first_name = first_name
    if last_name is not None:
        user.last_name = last_name
    if mobile_number is not None:
        user.mobile_number = mobile_number
    if password is not None:
        user.set_password(password)

    user.save()
    return Response(
        {"message": "User updated successfully."}, status=status.HTTP_200_OK
    )


# patch request to update participants data


@api_view(["PATCH"])
@permission_classes([IsTokenAuthenticated])
def update_participant(request):
    try:
        participant = models.Participant.objects.get(user=request.user)
    except models.Participant.DoesNotExist:
        return Response(
            {"error": "Participant not found."}, status=status.HTTP_404_NOT_FOUND
        )

    house = request.data.get("house")
    profile_picture = request.FILES.get("profile_picture")

    if house is not None:
        participant.house = house
    if profile_picture is not None:
        participant.profile_picture = profile_picture

    participant.save()
    return Response(
        {"message": "Participant updated successfully."}, status=status.HTTP_200_OK
    )


# patch project data


@api_view(["PATCH"])
@permission_classes([IsTokenAuthenticated])
def update_project(request):
    try:
        project = models.Project.objects.get(participant__user=request.user)
    except models.Project.DoesNotExist:
        return Response(
            {"error": "Project not found."}, status=status.HTTP_404_NOT_FOUND
        )

    project_idea_title = request.data.get("project_idea_title")
    project_idea_description = request.data.get("project_idea_description")
    project_experience = request.data.get("project_experience")
    project_video_link = request.data.get("project_video_link")

    if project_idea_title is not None:
        project.project_idea_title = project_idea_title
    if project_idea_description is not None:
        project.project_idea_description = project_idea_description
    if project_experience is not None:
        project.project_experience = project_experience
    if project_video_link is not None:
        project.project_video_link = project_video_link

    project.save()
    return Response(
        {"message": "Project updated successfully."}, status=status.HTTP_200_OK
    )


# update social links of user


@api_view(["PATCH"])
@permission_classes([IsTokenAuthenticated])
def update_social_links(request):
    try:
        social_links = models.SocialLinks.objects.get(user=request.user)
    except models.SocialLinks.DoesNotExist:
        return Response(
            {"error": "Social links not found."}, status=status.HTTP_404_NOT_FOUND
        )

    instagram = request.data.get("instagram")
    github = request.data.get("github")
    twitter = request.data.get("twitter")
    linkedin = request.data.get("linkedin")

    if instagram is not None:
        social_links.instagram = instagram
    if github is not None:
        social_links.github = github
    if twitter is not None:
        social_links.twitter = twitter
    if linkedin is not None:
        social_links.linkedin = linkedin

    social_links.save()
    return Response(
        {"message": "Social links updated successfully."}, status=status.HTTP_200_OK
    )


# update participants notifications


@api_view(["PATCH"])
@permission_classes([IsTokenAuthenticated])
def update_participant_notification(request, notification_id):
    try:
        notification = models.ParticipantNotification.objects.get(
            id=notification_id, participant__user=request.user
        )
    except models.ParticipantNotification.DoesNotExist:
        return Response(
            {"error": "Notification not found."}, status=status.HTTP_404_NOT_FOUND
        )

    is_read = request.data.get("is_read")

    if is_read is not None:
        notification.is_read = is_read

    notification.save()
    return Response(
        {"message": "Notification updated successfully."}, status=status.HTTP_200_OK
    )


@api_view(["PATCH"])
@permission_classes([IsTokenAuthenticated])
def update_all_details(request):
    try:
        user = request.user
        participant = user.participant_profile
        project = participant.participant_project
        social_links = user.social_links

    except models.ParticipantNotification.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    profile_picture = request.FILES.get("profile_picture")
    about = request.data.get("about")
    project_idea_title = request.data.get("project_idea_title")
    project_idea_description = request.data.get("project_idea_description")
    project_experience = request.data.get("project_experience")
    project_video_link = request.data.get("project_video_link")
    instagram = request.data.get("instagram")
    github = request.data.get("github")
    twitter = request.data.get("twitter")
    linkedin = request.data.get("linkedin")

    if project_idea_title is not None:
        project.project_idea_title = project_idea_title
    if project_idea_description is not None:
        project.project_idea_description = project_idea_description
    if project_experience is not None:
        project.project_experience = project_experience
    if project_video_link is not None:
        project.project_video_link = project_video_link

    if instagram is not None:
        social_links.instagram = instagram
    if github is not None:
        social_links.github = github
    if twitter is not None:
        social_links.twitter = twitter
    if linkedin is not None:
        social_links.linkedin = linkedin

    if profile_picture is not None:
        participant.profile_picture = profile_picture
    if about is not None:
        participant.about = about

    participant.save()
    project.save()
    social_links.save()
    return Response(
        {"message": f"User {user.email} updated successfully."},
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes([IsTokenAuthenticated])
def get_user_details(request):
    try:
        user = request.user
        social_links = user.social_links

    except models.ParticipantNotification.DoesNotExist:
        return Response(
            {"error": "User Or Social Links not found."},
            status=status.HTTP_404_NOT_FOUND,
        )
    if user.is_attendee:
        try:
            attendee = user.attendee
        except models.ParticipantNotification.DoesNotExist:
            return Response(
                {"error": "Attendee not found."}, status=status.HTTP_404_NOT_FOUND
            )
        return JsonResponse(
            {
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "date_joined": user.date_joined,
                "voted_project": attendee.voted_project.project.__dict__,
                "liked_projects": models.Like.objects.filter(
                    attendee=attendee
                ).values(),
                "instagram": social_links.instagram,
                "github": social_links.github,
                "twitter": social_links.twitter,
                "linkedin": social_links.linkedin,
            }
        )
    if user.is_participant:
        try:
            participant = user.participant_profile
            project = participant.participant_project
        except models.ParticipantNotification.DoesNotExist:
            return Response(
                {"error": "Participant Or Project not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return JsonResponse(
            {
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "date_joined": user.date_joined,
                "house": participant.house,
                "profile_picture": participant.profile_picture,
                "about": participant.about,
                "project_idea_title": participant.project_idea_title,
                "project_idea_description": participant.project_idea_description,
                "project_experience": participant.project_experience,
                "project_video_link": participant.project_video_link,
                "votes": project.vote_count.count,
                "likes": project.like_count.count,
                "liked_projects": models.Like.objects.filter(
                    participant=participant
                ).values(),
                "instagram": social_links.instagram,
                "github": social_links.github,
                "twitter": social_links.twitter,
                "linkedin": social_links.linkedin,
            }
        )


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def get_vote_count_for_all_projects(request):
    projects_vote_counts = models.VoteCount.objects.all()
    data_list = []
    for i in projects_vote_counts:
        temp_dict = {}
        temp_dict["participant_name"] = (i.project.participant.user.first_name,)
        temp_dict["participant_email"] = (i.project.participant.user.email,)
        temp_dict["project_idea_title"] = (i.project.project_idea_title,)
        temp_dict["project_idea_description"] = (i.project.project_idea_description,)
        temp_dict["project_experience"] = (i.project.project_experience,)
        temp_dict["project_video_link"] = (i.project.project_video_link,)
        temp_dict["vote_counts"] = (i.count,)
        data_list.append(temp_dict)

    return JsonResponse(data_list, safe=False)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def get_like_count_for_all_projects(request):
    projects_like_counts = models.LikeCount.objects.all()
    data_list = []
    for i in projects_like_counts:
        temp_dict = {}
        temp_dict["participant_name"] = (i.project.participant.user.first_name,)
        temp_dict["participant_email"] = (i.project.participant.user.email,)
        temp_dict["project_idea_title"] = (i.project.project_idea_title,)
        temp_dict["project_idea_description"] = (i.project.project_idea_description,)
        temp_dict["project_experience"] = (i.project.project_experience,)
        temp_dict["project_video_link"] = (i.project.project_video_link,)
        temp_dict["like_counts"] = (i.count,)
        data_list.append(temp_dict)

    return JsonResponse(data_list, safe=False)

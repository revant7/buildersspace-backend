import csv
from django.core.management.base import BaseCommand
from home import models
from django.core.files import File

User = models.User


class Command(BaseCommand):
    help = "Imports users and participants from a CSV file."

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="Path to the CSV file.")

    def handle(self, *args, **options):
        csv_file_path = options["csv_file"]

        try:
            with open(csv_file_path, "r", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    email = row.get("email")
                    first_name = row.get("first_name")
                    last_name = row.get("last_name", "")
                    mobile_number = row.get("mobile_number")
                    house = row.get("house")
                    project_idea_title = row.get("project_idea_title")
                    project_idea_description = row.get("project_idea_description")
                    project_experience = row.get("project_experience")
                    project_video_link = row.get("project_video_link")
                    profile_picture_path = row.get(
                        "profile_picture_path", None
                    )  # Path to the image if you have it.

                    if not email or not first_name or not mobile_number or not house:
                        self.stdout.write(
                            self.style.WARNING(
                                f"Skipping row due to missing required fields: {row}"
                            )
                        )
                        continue

                    try:
                        user, created = User.objects.get_or_create(
                            email=email,
                            defaults={
                                "first_name": first_name,
                                "last_name": last_name,
                                "mobile_number": mobile_number,
                                "is_participant": True,
                                "is_attendee": False,
                            },
                        )

                        if created:
                            password = User.objects.make_random_password()
                            user.set_password(password)
                            user.save()
                            self.stdout.write(
                                self.style.SUCCESS(f"Created user: {email}")
                            )
                        else:
                            self.stdout.write(
                                self.style.WARNING(f"User already exists: {email}")
                            )

                        participant, participant_created = (
                            models.Participant.objects.get_or_create(
                                user=user, defaults={"house": house}
                            )
                        )

                        if participant_created:
                            self.stdout.write(
                                self.style.SUCCESS(f"Created participant: {email}")
                            )

                            if profile_picture_path:
                                try:
                                    with open(profile_picture_path, "rb") as img_file:
                                        participant.profile_picture.save(
                                            f"{user.email}.jpg",
                                            File(img_file),
                                            save=True,
                                        )
                                        self.stdout.write(
                                            self.style.SUCCESS(
                                                f"Profile picture added for: {email}"
                                            )
                                        )
                                except FileNotFoundError:
                                    self.stdout.write(
                                        self.style.WARNING(
                                            f"Profile picture not found: {profile_picture_path} for {email}"
                                        )
                                    )
                            else:
                                self.stdout.write(
                                    self.style.WARNING(
                                        f"No profile picture path provided for: {email}"
                                    )
                                )

                            project, project_created = (
                                models.Project.objects.get_or_create(
                                    participant=participant,
                                    defaults={
                                        "project_idea_title": project_idea_title,
                                        "project_idea_description": project_idea_description,
                                        "project_experience": project_experience,
                                        "project_video_link": project_video_link,
                                    },
                                )
                            )
                            if project_created:
                                self.stdout.write(
                                    self.style.SUCCESS(f"Created project: {email}")
                                )
                                models.VoteCount(project=project).save()
                                models.LikeCount(project=project).save()
                                models.SocialLinks(user=user).save()
                                models.ParticipantNotification(
                                    participant=participant
                                ).save()
                            else:
                                self.stdout.write(
                                    self.style.WARNING(
                                        f"Project already exists for: {email}"
                                    )
                                )
                        else:
                            self.stdout.write(
                                self.style.WARNING(
                                    f"Participant already exists: {email}"
                                )
                            )

                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(f"Error processing row for {email}: {e}")
                        )

            self.stdout.write(
                self.style.SUCCESS("Successfully imported users and participants.")
            )

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"CSV file not found: {csv_file_path}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))

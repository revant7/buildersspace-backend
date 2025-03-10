import csv
from django.core.management.base import BaseCommand
from home import models
from django.core.files import File
from ... import utils

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
                    name = row.get("name", "").split()
                    if len(name) >= 2:
                        first_name = name[0]
                        last_name = " ".join(name[1:])
                    elif len(name) == 1:
                        first_name = name[0]
                        last_name = None
                    else:
                        first_name = utils.generate_random_password()
                        last_name = None
                    mobile_number = row.get("mobile_number")
                    domain = row.get("domain")
                    house = None
                    if domain == "Tech":
                        house = "Gryffindor"
                    elif domain == "Creative Arts":
                        house = "Hufflepuff"
                    elif domain == "Robotics":
                        house = "Ravenclaw"
                    elif domain == "Entrepreneurship":
                        house = "Phoenix"
                    elif (domain == "Entertainment") or (domain.strip() == "Other"):
                        house = "Slytherin"

                    project_idea_title = row.get("project_idea")
                    project_idea_description = row.get("project_idea_description")
                    project_experience = row.get("project_experience")
                    project_video_link = row.get("project_video_link")
                    about = row.get("about")
                    commudle_profile = row.get("commudle_profile")
                    social_media_links = row.get("social_media_links", "").split(",")
                    designation = row.get("designation")
                    location = row.get("location")
                    linkedin = ""
                    instagram = ""
                    twitter = ""
                    github = ""
                    if len(social_media_links) > 0:
                        for i in social_media_links:
                            i = i.strip()
                            if "linkedin" in i:
                                linkedin = i
                            elif "github" in i:
                                github = i
                            elif "x.com" in i:
                                twitter = i
                            elif "instagram" in i or "facebook" in i:
                                instagram = i

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
                            password = utils.generate_random_password()
                            user.set_password(password)
                            user.save()
                            self.stdout.write(
                                self.style.SUCCESS(f"Created user: {email}")
                            )
                            # utils.send_email(
                            #     subject="Test Email - Registration Successfull!",
                            #     message=f"Hi {name}, Your Registration is Successfull. \nDetails Are:- \nEmail:-{email}\nPassword:-{password}",
                            #     to_email=email,
                            # )

                        participant = models.Participant.objects.get(user=user)

                        participant.about = about
                        participant.house = house
                        participant.domain = domain
                        participant.designation = designation
                        participant.location = location

                        participant.save()

                        project = models.Project.objects.get(participant=participant)

                        project.project_idea_title = project_idea_title
                        project.project_idea_description = project_idea_description
                        project.project_experience = project_experience
                        project.project_video_link = project_video_link
                        project.save()

                        social_links_obj = models.SocialLinks.objects.get(user=user)
                        social_links_obj.github = github
                        social_links_obj.twitter = twitter
                        social_links_obj.instagram = instagram
                        social_links_obj.linkedin = linkedin
                        social_links_obj.commudle_profile = commudle_profile
                        social_links_obj.save()

                    except models.Participant.DoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(f"Participant does not exist: {email}")
                        )
                    except models.Project.DoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(f"Project does not exist: {email}")
                        )
                    except models.SocialLinks.DoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(f"Social links does not exist: {email}")
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

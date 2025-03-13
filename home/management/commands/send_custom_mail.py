import csv
from django.core.management.base import BaseCommand
from home import models
from django.core.files import File
from ... import utils
from datetime import datetime

User = models.User


class Command(BaseCommand):
    help = "Imports users and participants from a CSV file."

    def add_arguments(self, parser):
        parser.add_argument(
            "to_house",
            type=str,
            help="Specify A Particular House or All To send to all houses.",
        )

    def handle(self, *args, **options):
        to_house = options["to_house"]
        if to_house == "All":
            users = User.objects.all()
        elif to_house == "Gryffindor":
            pass
        elif to_house == "Hufflepuff":
            pass
        elif to_house == "Ravenclaw":
            pass
        elif to_house == "Phoenix":
            pass

        for i in users:
            noti = models.ParticipantNotification(
                participant=i.participant_profile,
                notification_title="Join Us for the Nights S1 Kickoff Session",
                notification_message=(
                    f"""

Get ready to kick off an exciting journey with Nights S1!

📅 Event Details:
Date & Time: 15 March 2025 at 9:30 PM
Kickoff Session Link: https://lu.ma/mp4dualo

Stay connected for all labs and sessions on our Discord Community: https://discord.gg/FHN8jkKt
We can’t wait to see you there!

Best regards,
Builder's Space


"""
                ),
                house=i.participant_profile.house,
            )
            noti.save()
            utils.send_email(
                subject="Join Us for the Nights S1 Kickoff Session",
                message="",
                to_email=i.email,
                html_template="emails/kickoff_reminder_template.html",
                context={
                    "name": i.first_name,
                },
            )
            self.stdout.write(
                self.style.SUCCESS(f"Successfully Created Notification for {i.email}.")
            )

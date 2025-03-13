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
            utils.send_email(
                subject="Welcome to Nights S1",
                message="",
                to_email=i.email,
                html_template="emails/kickoff_reminder_template.html",
                context={
                    "name": i.first_name,
                },
            )

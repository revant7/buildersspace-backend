import random, string
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from django.template.loader import render_to_string


def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits
    password = "".join(random.choice(characters) for i in range(length))
    return password


def send_email(
    subject="Test",
    message="Test Message",
    from_email="buildersspace9@gmail.com",
    from_name="BuildersSpace",
    to_email="revantstand@gmail.com",
    html_template=None,
    context=None,
    smtp_server="smtp.gmail.com",
    smtp_port=587,
    smtp_username="buildersspace9@gmail.com",
    smtp_password="nispghlsqzkknzvd",
):

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = formataddr((from_name, from_email))
    msg["To"] = to_email

    part1 = MIMEText(message, "plain")
    msg.attach(part1)

    if html_template:
        try:
            html_content = (
                render_to_string(html_template, context)
                if context
                else render_to_string(html_template)
            )
            part2 = MIMEText(html_content, "html")
            msg.attach(part2)
        except Exception as e:
            print(f"Error rendering HTML template: {e}")

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            if smtp_username and smtp_password:
                server.login(smtp_username, smtp_password)
            server.sendmail(from_email, to_email, msg.as_string())
        print(f"Email sent successfully to {to_email}")

    except Exception as e:
        print(f"Error sending email: {e}")

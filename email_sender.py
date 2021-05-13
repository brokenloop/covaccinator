import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from typing import List
from models import Place
from secret import (
    email_sender_account,
    email_sender_username,
    email_sender_password,
    email_smtp_server,
    email_smtp_port,
    email_recepients,  # List[str] email addresses to send notifications to
)


def get_booking_link(place: Place) -> str:
    return f"https://clients3.clicsante.ca/{place.establishment}"


def send_alert(place: Place, available_dates: List[str]):
    booking_link = get_booking_link(place)
    email_subject = f"Availability at {place.name_en}"
    email_body = f"There is an availability at the following place/date.\n\n Place Name: {place.name_en} \n\n Dates: {available_dates} \n\n Book here: {booking_link}"

    # login to email server
    server = smtplib.SMTP(email_smtp_server, email_smtp_port)
    server.starttls()
    server.login(email_sender_username, email_sender_password)
    # For loop, sending emails to all email recipients
    for recipient in email_recepients:
        print(f"Sending email to {recipient}")
        message = MIMEMultipart("alternative")
        message["From"] = email_sender_account
        message["To"] = recipient
        message["Subject"] = email_subject
        message.attach(MIMEText(email_body, "html"))
        text = message.as_string()
        server.sendmail(email_sender_account, recipient, text)
    # All emails sent, log out.
    server.quit()

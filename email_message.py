import smtplib
import os

MY_EMAIL = os.environ.get('EMAIL_ADDRESS')
MY_PASS = os.environ.get('EMAIL_PASS')


def email_message(message):
    with smtplib.SMTP_SSL("smtp.gmail.com") as connection:
        connection.login(user=MY_EMAIL, password=MY_PASS)
        connection.sendmail(
            from_addr="python@flight-crew.org",
            to_addrs=MY_EMAIL,
            msg=f"Subject: Precipitation Alert!"
                f"\n\n{message}"
        )

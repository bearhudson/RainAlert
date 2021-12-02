import smtplib
import os

MY_EMAIL = os.environ.get('MY_EMAIL')
MY_PASS = os.environ.get('MY_PASS')
MY_SERVER = os.environ.get("MY_SERVER")
MY_FROM = os.environ.get('MY_FROM')


def email_message(message):
    with smtplib.SMTP_SSL(MY_SERVER) as connection:
        connection.login(user=MY_EMAIL, password=MY_PASS)
        connection.sendmail(
            from_addr=MY_FROM,
            to_addrs=MY_EMAIL,
            msg=f"Subject: Precipitation Alert!"
                f"\n\n{message}"
        )

from django.core import mail
from DjangoApp1.settings import EMAIL_BACKEND

""" CONSTANT """

connection = mail.get_connection(EMAIL_BACKEND)
connection.open()


def create_new_email(subject, message, _from, _to):
    """
    Create a new email.
    """

    email = mail.EmailMessage(
        subject=subject,
        body=message,
        from_email=_from,
        to=[_to],
        connection=connection
    )

    email.send()

    connection.send_messages([email])
    connection.close()

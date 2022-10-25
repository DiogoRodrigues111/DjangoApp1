from django.core import mail


class SendEmail(mail.EmailMessage):
    """
    Send an Email.

    Note:
        Extended to django.core.mail
    """

    def create_new_email(self, message, _from, _to):
        """
        Create a new email.
        """

        """ Specify arguments for mail. """

        self.from_email = _from
        self.to = _to
        self.body = message
        self.send()

        return self.message()

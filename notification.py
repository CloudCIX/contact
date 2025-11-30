# stdlib
import logging
import re
# libs
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
# local
from .models import OpportunityHistory

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class OpportunityHistoryNotification():  # pragma: no cover
    """
    When an Opportunity history is created with type email, this class will send a copy of the message
    (body) to those in request.
    """

    def send(self, user, opportunity_history: OpportunityHistory):
        """
        Send email to those in request
        """

        if settings.TESTING:
            return None

        logger.info(f'Sending email for Opportunity History ID #{opportunity_history["id"]}')

        subject = opportunity_history['heading']
        html_message = opportunity_history['message']
        html_message += f'<hr>This message was sent by {user.first_name} {user.surname} <{user.email}>'
        html_match = re.compile('<br>|<br />|<p>|</p>|<table>|</tr>|</table>|<hr>', re.IGNORECASE)

        message = html_match.split(html_message)
        message = '\n'.join(message)
        message = strip_tags(message)

        live_env = getattr(settings, 'PRODUCTION_DEPLOYMENT', False)
        if live_env:
            to = opportunity_history['to']
            cc = opportunity_history['cc']
        else:
            to = ['developers@cloudcix.com']
            cc = []

        # Create and send the email object
        email = EmailMultiAlternatives(
            from_email=settings.EMAIL_HOST_USER,
            to=to,
            cc=cc,
            reply_to=[opportunity_history.get('reply_to', user.email)],
            subject=subject,
            body=message,
        )
        try:
            email.send()
        except Exception as e:
            logger.error(
                f'Error occurred when sending Opportunity History Email to {to} for Opportunity History ID '
                f'{opportunity_history["id"]}: Error: {e}',
            )

        return None

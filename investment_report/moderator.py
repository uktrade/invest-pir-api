from moderation import moderation
from moderation.moderator import GenericModerator

from investment_report.models import PDFSection


class Moderator(GenericModerator):
    notify_user = False
    auto_approve_for_superusers = False
    auto_approve_for_staff = False


for klass in PDFSection.__subclasses__():
    moderation.register(klass, Moderator)

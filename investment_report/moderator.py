from moderation import moderation
from moderation.moderator import GenericModerator

from investment_report.models import PDFSection


class Moderator(GenericModerator):
    notify_user = True
    auto_approve_for_superusers = False
    auto_approve_for_staff = False
    keep_history = False
    notify_moderator = True


for klass in PDFSection.__subclasses__():
    moderation.register(klass, Moderator)

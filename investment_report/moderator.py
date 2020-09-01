from moderation import moderation
from moderation.moderator import GenericModerator

from investment_report import models


class Moderator(GenericModerator):
    notify_user = True
    auto_approve_for_superusers = False
    auto_approve_for_staff = False
    keep_history = False
    notify_moderator = True


for model_class in [
    models.FrontPage,
    models.SectorOverview,
    models.KillerFacts,
    models.MacroContextBetweenCountries,
    models.UKMarketOverview,
    models.UKBusinessInfo,
    models.UKGeographicOverview,
    models.TalentAndEducationBySector,
    models.SectorInitiatives,
    models.RDandInnovation,
    models.NetworkAndSupport,
    models.RDandInnovationCaseStudy,
    models.VideoCaseStudy,
    models.WhoIsHere,
    models.ServicesOfferedByDIT,
    models.CallToAction,
    models.Contact,
    models.CaseStudySector,
    models.HowWeCanHelp,
    models.SmartWorkforceSector,
    models.LastPage
]:
    moderation.register(model_class, Moderator)

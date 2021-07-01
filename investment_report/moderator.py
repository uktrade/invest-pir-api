from moderation import moderation

from investment_report import models


# class Moderator(GenericModerator):
#     notify_user = True
#     auto_approve_for_superusers = False
#     auto_approve_for_staff = False
#     keep_history = False
#     notify_moderator = True


for model_class in [
    # models.FrontPage,
    # models.ContentsPage,
    # models.SectorOverview,
    # models.KillerFacts,
    # models.MacroContextBetweenCountries,
    # models.UKMarketOverview,
    # models.SectorInitiatives,
    # models.CaseStudySector,
    # models.HowWeCanHelp,
    # models.SmartWorkforceSector,
    # models.LastPage,
    models.MarketContact,
]:
        moderation.register(model_class)

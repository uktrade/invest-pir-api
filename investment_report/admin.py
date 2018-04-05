# virtually admin.yp

from investment_report.models import (
    Sector, Market,
    SectorOverview
)

from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register
)

from wagtail.contrib.modeladmin.helpers.permission import PermissionHelper



class SingletonPage(PermissionHelper):
    """
    Allows the admin to only create a single copy of a page.
    """

    def user_can_create(self, user):
        """
        Return a boolean to indicate whether `user` is permitted to create new
        instances of `self.model`
        """
        return self.model.objects.count() < 1


class SectorOverViewAdmin(ModelAdmin):
    model = SectorOverview
    menu_label = 'Sector Overview'


class SectorAdmin(ModelAdmin):
    model = Sector
    menu_label = 'Sector List'


class MarketAdmin(ModelAdmin):
    model = Market
    menu_label = 'Market List'


modeladmin_register(SectorOverViewAdmin)
modeladmin_register(SectorAdmin)
modeladmin_register(MarketAdmin)

# virtually admin.yp

from investment_report.models import (
    PDFSection, Market, Sector, MarketLogo, SectorLogo
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


for klass in PDFSection.__subclasses__():
    """
    I can't be arrsed to create another 14 nearly identical classes

    Auto generate the admin for PDF section
    """
    Admin = type(
        '{}Admin'.format(klass),
        (ModelAdmin, ),
        {
            'model': klass,
            'permission_helper_class': (
                SingletonPage if klass.SINGLETON else PermissionHelper
            ),
            'menu_order': klass.SECTION,
            'menu_label': klass.NAME
        }
    )

    modeladmin_register(Admin)


class MarketAdmin(ModelAdmin):
    model = Market


class SectorAdmin(ModelAdmin):
    model = Sector


class MarketLogoAdmin(ModelAdmin):
    model = MarketLogo


class SectorLogoAdmin(ModelAdmin):
    model = SectorLogo


modeladmin_register(MarketAdmin)
modeladmin_register(SectorAdmin)
modeladmin_register(MarketLogoAdmin)
modeladmin_register(SectorLogoAdmin)

# virtually admin.yp

from investment_report.models import FrontPage

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


class FrontPageAdmin(ModelAdmin):
    model = FrontPage
    permission_helper_class = SingletonPage
    menu_label = 'Front Page'


modeladmin_register(FrontPageAdmin)

# Based on bakerydemo
from django import template

from wagtail.core.models import Page


register = template.Library()
# https://docs.djangoproject.com/en/1.9/howto/custom-template-tags/


@register.simple_tag(takes_context=True)
def get_site_root(context):
    # This returns a core.Page. The main menu needs to have the site.root_page
    # defined else will return an object attribute error ('str' object has no
    # attribute 'get_children')
    return context['request'].site.root_page


def is_active(page, current_page):
    # To give us active state on main navigation
    return current_page.url.startswith(page.url) and current_page


def get_menu_pages(context, parent, calling_page=None):
    root = get_site_root(context)
    menuitems = parent.get_children().live().in_menu()
    if parent == root:
        menuitems |= Page.objects.filter(pk=root.id).live().in_menu()

    for menuitem in menuitems:
        if menuitem == root:
            # Treat root menuitem like it is on the next level
            # must match urls exactly as all URLs will start with homepage URL
            menuitem.active = (
                (calling_page.url == menuitem.url)
                if calling_page else False
            )
        else:
            # We don't directly check if calling_page is None since the
            # template engine can pass an empty string to calling_page
            # if the variable passed as calling_page does not exist.
            menuitem.active = ((calling_page.url.startswith(menuitem.url)
                               if calling_page else False))
    return menuitems


@register.inclusion_tag('tags/top_menu.html', takes_context=True)
def nav_menu(context, parent, calling_page=None, item_class="nav-item"):
    menuitems = get_menu_pages(context, parent, calling_page)
    return {
        'calling_page': calling_page,
        'menuitems': menuitems,
        'item_class': item_class,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }

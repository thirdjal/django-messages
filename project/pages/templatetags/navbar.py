from django import template

from project.pages.models import ContentBlock, Page

register = template.Library()


@register.simple_tag(takes_context=True)
def get_nav_links(context):
    return Page.objects.filter(
        shown_in_navbar=True,
        base__isnull=True,
        content_blocks__in=ContentBlock.objects.get_visible(user=context["user"]),
    ).distinct

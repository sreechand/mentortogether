from django import template
from mentortogether.cms.models import Notice

register = template.Library()

@register.inclusion_tag('cms_notice.html')
def cms_notices(board):
    """
    Renders the notices for a given board name.
    """
    notices = Notice.objects.filter(board__exact=board)
    return { 'notices' : notices }


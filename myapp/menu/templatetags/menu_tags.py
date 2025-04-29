from django import template
from myapp.menu.models import MenuItem
from myapp.menu.utils import build_menu_tree
import logging

logger = logging.getLogger(__name__)
register = template.Library()


@register.inclusion_tag('menu.html', takes_context=True)
def draw_menu(context, menu_name):
    try:
        request = context.get('request')
        if not request:
            logger.warning("Request object missing in context")
            return {'tree': []}

        active_url = request.path
        
        items = MenuItem.objects.filter(
            menu_name=menu_name
        ).select_related('parent').order_by('order')
        
        if not items.exists():
            logger.debug(f"No items found for menu '{menu_name}'")
            return {'tree': []}

        tree = build_menu_tree(items, active_url)
        
        return {
            'tree': tree,
            'menu_name': menu_name  
        }

    except Exception as e:
        logger.error(f"Error rendering menu '{menu_name}': {str(e)}")
        return {'tree': []}
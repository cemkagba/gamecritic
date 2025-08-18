"""
Custom template tags and filters for the blog app.
"""

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def safe_image_url(image_field):
    """
    Safely get image URL, return None if no image exists.
    Usage: {{ game.image|safe_image_url }}
    """
    try:
        if image_field and hasattr(image_field, 'url'):
            return image_field.url
    except (ValueError, AttributeError):
        pass
    return None


@register.inclusion_tag('partials/_image_placeholder.html')
def image_or_placeholder(image_field, alt_text="", css_class="", placeholder_text="No Image"):
    """
    Render an image or placeholder if no image exists.
    Usage: {% image_or_placeholder game.image game.title "w-32 h-24" %}
    """
    image_url = safe_image_url(image_field)
    return {
        'image_url': image_url,
        'alt_text': alt_text,
        'css_class': css_class,
        'placeholder_text': placeholder_text,
    }


@register.filter
def rating_color(rating):
    """
    Return CSS color class based on rating value.
    Usage: {{ rating|rating_color }}
    """
    try:
        rating = float(rating) if rating else 0
        if rating >= 4.0:
            return 'text-green-600 bg-green-600'
        elif rating >= 3.0:
            return 'text-yellow-600 bg-yellow-600'
        elif rating >= 2.0:
            return 'text-orange-600 bg-orange-600'
        elif rating > 0:
            return 'text-red-600 bg-red-600'
        else:
            return 'text-gray-500 bg-gray-400'
    except (ValueError, TypeError):
        return 'text-gray-500 bg-gray-400'


@register.filter
def rating_text(rating):
    """
    Return descriptive text based on rating value.
    Usage: {{ rating|rating_text }}
    """
    try:
        rating = float(rating) if rating else 0
        if rating >= 4.5:
            return 'Fantastic'
        elif rating >= 4.0:
            return 'Great'
        elif rating >= 3.0:
            return 'Okay'
        elif rating >= 2.0:
            return 'Meh'
        elif rating > 0:
            return 'Awful'
        else:
            return 'No Score'
    except (ValueError, TypeError):
        return 'No Score'

# store/templatetags/store_extras.py
from django import template

register = template.Library()

@register.filter
def average(queryset, field_name):
    """
    Calculate average of a numeric field (like rating) in a queryset.
    Example usage in template: {{ product.reviews.all|average:"rating" }}
    """
    total = count = 0
    for obj in queryset:
        value = getattr(obj, field_name, None)
        if value is not None:
            total += value
            count += 1
    return round(total / count, 1) if count > 0 else 0

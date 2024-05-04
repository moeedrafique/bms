# templatetags/user_tags.py

from django import template

register = template.Library()

@register.filter
def user_type_label(user_type):
    ROLE_CHOICES = {
        1: "Admin",
        2: "Store Manager",
        3: "Staff",
        # Add more choices as needed
    }
    return ROLE_CHOICES.get(user_type, "Unknown")

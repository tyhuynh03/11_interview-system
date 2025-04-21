from django import template
import re

register = template.Library()

@register.filter
def format_bullets(text):
    # Thay thế dấu gạch ngang đầu dòng bằng dấu chấm tròn
    return re.sub(r'^\s*-\s+', '• ', text, flags=re.MULTILINE)
from django import template
from django.template.defaultfilters import stringfilter

import markdown as md

register = template.Library()

@register.filter()
@stringfilter
def markdown(text):
  return md.markdown(text, extensions=['markdown.extensions.fenced_code'])
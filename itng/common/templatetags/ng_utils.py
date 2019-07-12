
import re

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_text
from ordered_set import OrderedSet

register = template.Library()


@register.filter
def required(field):
    """
    Return 'required' as a string if the BoundField's underlying field is required.
    """
    return "required" if field.field.required else ""


@register.filter
def add_class(value, css_classes):
    """
    Add a single or multiple css classes to a form widget. To add multiple classes, pass
    them as a whitespace delimited string. eg, {{ field|add_class:"foo bar" }}
    """
    if not css_classes:
        return value

    widget = value.field.widget
    orig_classes = OrderedSet(widget.attrs.get('class', '').split())
    new_classes = OrderedSet(css_classes.split())

    widget.attrs['class'] = " ".join(orig_classes | new_classes)
    return value


@register.simple_tag(takes_context=True)
def isactive(context, url, active='active', inactive='', exact=False):
    """
    A ternary tag for whether a URL is 'active'. An active URL is defined as matching
    the current request URL. The default behavior is to match the beginning of the URL.
    For example, if `url` is '/some/path' and the current request URL is
    '/some/path/subpath', then the URL is considered active. If `exact` is set to True,
    then the URL's must match exactly.

    Example::

        {% url 'named-url' as named_url %}
        <div class="{% isactive named_url 'active' 'inactive' %}">
        </div>

    """
    request_url = context['request'].path_info
    if (request_url == url if exact else request_url.startswith(url)):
        return active
    return inactive


# def ifactive
# refer to {% ifequal %} implementation because it doesn't perform {% if %} condition parsing


# Originally from: https://djangosnippets.org/snippets/1519/
CONSONANT_SOUND = re.compile(r'''one(![ir])''', re.IGNORECASE | re.VERBOSE)
VOWEL_SOUND = re.compile(r'''[aeio]|u([aeiou]|[^n][^aeiou]|ni[^dmnl]|nil[^l])|h(ier|onest|onou?r|ors\b|our(!i))|[fhlmnrsx]\b''', re.IGNORECASE | re.VERBOSE)

@register.filter
def an(text):
    text = force_text(text)
    match = not CONSONANT_SOUND.match(text) and VOWEL_SOUND.match(text)

    return '%s %s' % ('an' if match else 'a', text)

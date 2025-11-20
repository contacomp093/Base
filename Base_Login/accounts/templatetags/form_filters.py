import re
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


def ensure_html(field_or_html):
    """
    Si es BoundField, renderea el widget.
    Si ya es HTML (SafeString), lo retorna igual.
    """
    try:
        return field_or_html.as_widget()
    except AttributeError:
        return str(field_or_html)


def modify_attr(html, attr, value):
    """
    Inserta o reemplaza un atributo en HTML.
    """
    # Reemplazar atributo existente
    if f'{attr}="' in html:
        html = re.sub(rf'{attr}="([^"]*)"', f'{attr}="{value}"', html)
    else:
        # Insertarlo antes del cierre del tag
        html = html.replace(">", f' {attr}="{value}">')
    return html


@register.filter(name="add_class")
def add_class(field, css_class):
    html = ensure_html(field)
    html = modify_attr(html, "class", css_class)
    return mark_safe(html)


@register.filter(name="add_placeholder")
def add_placeholder(field, text):
    html = ensure_html(field)
    html = modify_attr(html, "placeholder", text)
    return mark_safe(html)


@register.filter(name="add_attr")
def add_attr(field, arg):
    """
    Uso: add_attr:'type=tel'
    """
    if "=" not in arg:
        return field

    key, value = arg.split("=", 1)
    html = ensure_html(field)
    html = modify_attr(html, key, value)
    return mark_safe(html)

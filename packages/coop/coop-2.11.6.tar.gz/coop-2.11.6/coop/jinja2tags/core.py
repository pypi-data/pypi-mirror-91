import json
import re

import jinja2
import jinja2.ext
from django.conf import settings
from django.contrib.messages.context_processors import get_messages
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.utils import flatatt
from django.template.defaultfilters import date, linebreaks_filter, linebreaksbr, time
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import format_html, mark_safe
from wagtail.core.models import Page, Site
from webpack_loader.templatetags.webpack_loader import render_bundle


def add_form_class(bound_field, new_classes):
    """Add a class to a django form field widget"""
    attrs = bound_field.field.widget.attrs
    classes = sorted(set(attrs.get('class', '').split() + new_classes.split()))
    attrs['class'] = ' '.join(classes)
    return bound_field


def add_form_attributes(bound_field, attributes={}):
    """Add 1 or more attributes to a django form field widget"""
    bound_field.field.widget.attrs.update(attributes)
    return bound_field


def include_static(path):
    """
    Include the contents of a file that has been compiled into the static directory
    """
    fullpath = finders.find(path)
    if fullpath is None:
        raise ValueError("Could not find file %s" % path)

    with open(fullpath, "r") as f:
        return f.read()


def debug_variable(variable):
    """Print all the fields available on a variable"""
    return format_html('<pre>{}</pre>', dir(variable))


@jinja2.contextfunction
def csrf_field(context):
    """Print the hidden CSRF token field"""
    csrf_token = context.get('csrf_token')
    if not csrf_token or csrf_token == 'NOTPROVIDED':
        return format_html("")

    return format_html("<input{}>", flatatt({
        'type': 'hidden',
        'name': 'csrfmiddlewaretoken',
        'value': csrf_token}))


def url(name, *args, **kwargs):
    """Reverse a URL name. Alias of ``django.core.urlresolvers.reverse``"""
    return reverse(name, args=args or None, kwargs=kwargs or None)


@jinja2.contextfunction
def site_root(context):
    """Get the root page for the site"""
    # This lookup will be cached on the intermediary objects, so this will only
    # hit the DB once per request
    request = context['request']
    return Site.find_for_request(request).root_page.specific


def svg_inline(name):
    """
    Inline an SVG image. SVG images are expected to be a template, not kept in
    the static files
    """
    return mark_safe(render_to_string('svgs/%s.svg' % name))


@jinja2.contextfunction
def breadcrumbs(context, page=None):
    """Print the top navigation menu for this site"""
    request = context.get('request')
    root = site_root(context)
    if page is None:
        page = context.get('page')
    ancestors = page.get_ancestors().filter(depth__gte=root.depth)

    return jinja2.Markup(render_to_string('tags/breadcrumbs.html', {
        'page': page,
        'ancestors': ancestors,
        'request': request,
    }))


def js_context(key, value):
    """ Adds variables to the window for use by other scripts. """
    return format_html('window.appData["{0}"] = {1};'.format(key.upper(), json.dumps(value)))


def model_classname(model_or_instance):
    """
    Generate a CSS class name from a Page model

    Usage::

        <html class="{{ self|model_classname }}">
    """
    if isinstance(model_or_instance, Page):
        model_or_instance = model_or_instance.content_type.model_class()

    try:
        meta = model_or_instance._meta
        return 'page-{0}-{1}'.format(meta.app_label, meta.model_name)
    except AttributeError:
        return ''


@jinja2.contextfunction
def messages(context):
    """Get any messages from django.contrib.messages framework"""
    return get_messages(context.get('request'))


def json_dumps(value):
    """
    Dump the value to a JSON string. Useful when sending values to JavaScript
    """
    return jinja2.Markup(json.dumps(value, cls=DjangoJSONEncoder))


@jinja2.contextfunction
def qs(context, get=None, **kwargs):
    """
    Update a querydict with new values, and return it as a URL encoded string.
    Pass in the current ``request.GET``, and any items to set as keyword
    arguments. If a key has a value of ``None``, that key is removed from the
    querydict.

    The querydict is grabbed from ``request`.GET` in the context by default,
    but an alternative can be provided as the first positional argument.

    >>> request.GET.urlencode()
    "page=1&foo=bar"
    >>> qs(request.GET, page=2, baz="quux", foo=None)
    "page=2&baz=quux"
    """
    if get is None:
        get = context['request'].GET

    get = get.copy()
    for key, value in kwargs.items():
        if value is None:
            # Delete keys if value is None
            get.pop(key, None)
        else:
            get[key] = value
    return get.urlencode()


not_digit_re = re.compile(r'[^0-9+]+')


def tel(value):
    return 'tel:{}'.format(not_digit_re.sub('-', value).strip('-'))


def source_tag(image, media, normal_spec, retina_spec):
    return format_html(
        '<source media="{media}" srcset="{normal_image_url}, {retina_image_url} 2x">',
        media=media,
        normal_image_url=image.get_rendition(normal_spec).url,
        retina_image_url=image.get_rendition(retina_spec).url,
    )


def render_honeypot_field():
    return jinja2.Markup(render_to_string('honeypot/honeypot_field.html', {
        'fieldname': settings.HONEYPOT_FIELD_NAME,
        'value': ''
    }))


@jinja2.contextfunction
def analytics_js(context):
    hide: bool = settings.DEBUG
    if request := context.get('request'):
        hide |= getattr(request, 'preview', False)
    if not hide:
        return mark_safe(
            '<script defer src="https://stats.neonjungle.com.au/analytics.js"></script>')
    return ''


class Extension(jinja2.ext.Extension):
    def __init__(self, environment):
        super().__init__(environment)

        self.environment.globals.update({
            'breadcrumbs': breadcrumbs,
            'site_root': site_root,
            'csrf_field': csrf_field,
            'static': staticfiles_storage.url,
            'include_static': include_static,
            'render_bundle': render_bundle,
            'url': url,
            'svg': svg_inline,
            'js_context': js_context,
            'model_classname': model_classname,
            'messages': messages,
            'DEBUG': settings.DEBUG,
            'qs': qs,
            'pic_src': source_tag,
            'render_honeypot_field': render_honeypot_field,
            'analytics_js': analytics_js,
        })

        self.environment.filters.update({
            'model_classname': model_classname,
            'add_form_class': add_form_class,
            'add_form_attributes': add_form_attributes,
            'debug_variable': debug_variable,
            'br': linebreaksbr,
            'p': linebreaks_filter,
            'json': json_dumps,
            'tel': tel,
            'time_format': time,
            'date_format': date
        })

from django.utils.translation import gettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import Heading


@plugin_pool.register_plugin
class HeadingPlugin(CMSPluginBase):
    model = Heading
    name = _('Heading')
    render_template = "djangocms_headings/heading.html"

    fieldsets = (
        (None, {
            'fields': ('heading', 'text')
        }),
        (_('Options'), {
            'fields': ('css_classes', 'html_id'),
            'classes': ('collapse', )
        }),
    )

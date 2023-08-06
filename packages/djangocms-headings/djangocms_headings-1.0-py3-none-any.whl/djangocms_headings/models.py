from django.db import models
from django.utils.html import mark_safe

from cms.models.pluginmodel import CMSPlugin


class Heading(CMSPlugin):
    HEADINGS = [
        ('h1', 'h1'),
        ('h2', 'h2'),
        ('h3', 'h3'),
        ('h4', 'h4'),
        ('h5', 'h5'),
        ('h6', 'h6'),
    ]

    heading = models.CharField(max_length=2, choices=HEADINGS, default='h2')
    text = models.CharField(max_length=200)

    css_classes = models.CharField(max_length=100, blank=True)
    html_id = models.SlugField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.text} ({self.heading})'

    def get_css_classes(self):
        if self.css_classes:
            return mark_safe(f' class="{self.css_classes}"')
        return ''

    def get_html_id(self):
        if self.html_id:
            return mark_safe(f' id="{self.html_id}"')
        return ''

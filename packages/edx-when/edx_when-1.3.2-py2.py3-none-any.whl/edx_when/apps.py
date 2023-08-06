# -*- coding: utf-8 -*-
"""
edx_when Django application initialization.
"""

from django.apps import AppConfig


class EdxWhenConfig(AppConfig):
    """
    Configuration for the edx_when Django application.
    """

    name = 'edx_when'
    verbose_name = "edX When"
    plugin_app = {
        'url_config': {
            'lms.djangoapp': {
                'namespace': u'edx_when',
                'regex': u'^api/',
                'relative_path': u'urls',
            },
        }
    }

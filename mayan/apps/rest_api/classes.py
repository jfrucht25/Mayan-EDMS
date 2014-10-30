from __future__ import absolute_import

from django.conf.urls import include, patterns, url
from django.utils.importlib import import_module

from common.utils import load_backend


class APIEndPoint(object):
    _registry = {}

    @classmethod
    def get_all(cls):
        return cls._registry.values()

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    def __unicode__(self):
        return unicode(self.name)

    def __init__(self, name, app_name=None):
        self.name = name
        self.endpoints = []
        try:
            api_urls = load_backend('{}.urls.api_urls'.format(app_name or name))
        except Exception as exception:
            # Ignore import time errors
            pass
        else:
            self.register_urls(api_urls)

        self.__class__._registry[name] = self

    def register_urls(self, urlpatterns):
        from .urls import version_0_urlpatterns
        endpoint_urls = patterns('',
            url(r'^%s/' % self.name, include(urlpatterns)),
        )

        version_0_urlpatterns += endpoint_urls

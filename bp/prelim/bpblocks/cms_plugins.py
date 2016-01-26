# -*- coding: utf-8 -*-

from cms.models.pluginmodel import CMSPlugin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext as _
from .models import RawHtmlCode


class TopLogoPlugin(CMSPluginBase):
    model = CMSPlugin
    name = _(u"Top logo")
    render_template = "toplogo.html"
    text_enabled = True
    allow_children = True

    def render(self, context, instance, placeholder):
        context.update({
            'instance': instance,
            'placeholder': placeholder
        })
        return context


class RightHeaderPlugin(CMSPluginBase):
    model = CMSPlugin
    name = _(u"Right Header")
    render_template = "rightheader.html"
    text_enabled = True
    allow_children = True

    def render(self, context, instance, placeholder):
        context.update({
            'instance': instance,
            'placeholder': placeholder
        })
        return context


class SyncHtmlCode(CMSPluginBase):
    model = RawHtmlCode
    name = _(u"Raw html")
    render_template = "synccode.html"
    text_enabled = True

    def render(self, context, instance, placeholder):
        context.update({
            'instance': instance,
            'placeholder': placeholder
        })
        return context


plugin_pool.register_plugin(TopLogoPlugin)
plugin_pool.register_plugin(RightHeaderPlugin)
plugin_pool.register_plugin(SyncHtmlCode)

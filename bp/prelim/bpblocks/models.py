from django.db import models


from cms.models.pluginmodel import CMSPlugin
from django.utils.encoding import python_2_unicode_compatible



@python_2_unicode_compatible
class RawHtmlCode(CMSPlugin):
    code = models.TextField(blank=True, default="")
    
    def __str__(self):
        return self.code[:30]
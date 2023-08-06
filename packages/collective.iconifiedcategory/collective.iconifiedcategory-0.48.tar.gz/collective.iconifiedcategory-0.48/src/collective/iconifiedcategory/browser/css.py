# -*- coding: utf-8 -*-
"""
collective.iconifiedcategory
----------------------------

Created by mpeeters
:license: GPL, see LICENCE.txt for more details.
"""

from Products.Five import BrowserView

from collective.iconifiedcategory import utils


class IconifiedCategory(BrowserView):

    def __call__(self, *args, **kwargs):
        self.request.response.setHeader('Content-Type', 'text/css')
        content = []
        css = (u".{0} {{ padding-left: 1.4em; background: "
               u"transparent url('{1}') no-repeat top left; "
               u"background-size: contain; }}")
        if utils.has_config_root(self.context) is False:
            return ''
        categories = utils.get_categories(self.context)
        for category in categories:
            obj = category._unrestrictedGetObject()
            category_id = utils.calculate_category_id(obj)
            url = u'{0}/@@download'.format(obj.absolute_url())
            content.append(css.format(utils.format_id_css(category_id), url))
        return ' '.join(content)

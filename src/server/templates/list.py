# coding: UTF-8

import urlparse

template = {
    'attachment': {
        'type': 'template',
        'payload': {
            'template_type': 'generic',
            'elements': []
        }
    }
}


class ListMessage:
    def __init__(self, compact=True):
        self.template = template
        self.elements = []
        if compact:
            self.template['attachment']['payload']['top_element_style'] = 'compact'

    def add_element(self, title='', subtitle='', url='', image_url='', buttons=None):
        if buttons is None:
            buttons = []

        element = {
            'title': title,
            'subtitle': subtitle,
            'image_url': image_url,
            'default_action': {
                'type': 'web_url',
                'messenger_extensions': True,
                'url': url,
                'webview_height_ratio': 'full',
                'fallback_url': urlparse.urljoin(url, '/')
            },
            'buttons': buttons
        }
        self.elements.append(element)

    def get_message(self):
        self.template['attachment']['payload']['elements'] = self.elements
        return self.template

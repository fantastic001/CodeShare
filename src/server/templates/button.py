# coding: UTF-8

class UrlButton:
	def __init__(self, url, title):
		self.template = {'type': 'web_url', 'webview_height_ratio': 'full', 'url': url, 'title': title}
		
	def get_button(self):
		return self.template
		
	def get_standalone_button(self, text):
		return {
			'attachment': {
				'type': 'template',
				'payload': {
					'template_type': 'button',
					"text": text,
					"buttons": [self.template]
				}
			}
		}


class PostbackButton:
    def __init__(self, title, payload):
        self.template = {'type': 'postback', 'payload': payload, 'title': title}

    def get_button(self):
        return self.template

		
class CallButton:
	def __init__(self, text, title, number):
		self.template = {
			'attachment': {
				'type': 'template',
				'payload': {
					'template_type': 'button',
					"text": text,
					"buttons":[
					{
						"type": "phone_number",
						"title": title,
						"payload": number
					}
					]
				}
			}
		}
		
	def get_button(self):
		return self.template


class QuickReply:
	def __init__(self, text):
		self.text = text
		self.elements = []
		
	def addButton(self, title, payload):
		self.elements.append({
			"content_type":"text",
			"title": title,
			"payload": payload
		} )
	
	def addLocation(self):
		self.elements.append( { "content_type": "location" } )
		
	def get_button(self):
		return {
			"text": self.text,
			"quick_replies": self.elements
		}
		
		
		
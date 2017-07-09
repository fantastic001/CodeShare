# coding: UTF-8

import api
import config
import textData
from flask import Flask, request
from templates.text import *
from templates.button import UrlButton
from api.witclient import client

app = Flask(__name__)


@app.route('/')
def about():
    return "Telenor Bot"


@app.route('/webhook/', methods=['GET'])
def verify():
    if request.args.get('hub.verify_token') == config.VERIFY_TOKEN:
        return request.args.get('hub.challenge')
    else:
        return "Error, wrong verification token"


@app.route('/webhook/', methods=['POST'])
def main():
    data = request.get_json()
    messaging_events = data['entry'][0]['messaging']

    for event in messaging_events:
		sender = event['sender']['id']
		api.message_seen(sender)
		api.set_typing_on(sender)
		if 'postback' in event:
			payload = event['postback']['payload']
			if payload == config.GET_STARTED_PAYLOAD:	# start conversation
				message = TextMessage(textData.GET_STARTED_PAYLOAD_MESSAGE)
				api.send_message(sender, message.get_message())
			elif payload.startswith(config.PAYLOAD_PHONE_PRICE):
				phone_id = payload[len(config.PAYLOAD_PHONE_PRICE):]
				phone_id = phone_id.replace('_', ' ')
				# vrsi se pretraga baze po phone_id
				message = TextMessage("Cena telefona " + phone_id + " (obaveza na 24 rate) je:\n1.024 din\nitd.")
				api.send_message(sender, message.get_message())
		elif 'message' in event:
			if 'quick_reply' in event['message']:
				payload = event['message']['quick_reply']['payload']
				if payload == config.PAYLOAD_SHOW_HELP:
					message = TextMessage(textData.PAYLOAD_SHOW_HELP_MESSAGE)
					api.send_message(sender, message.get_message())
			elif 'text' in event['message']:
				text = event['message']['text']
				try:
					client.run_actions(sender, text)  # pozivamo WIT da odradi svoje
				except:
					message = TextMessage("Ne razumem Vas, možete li ponovo objasniti?")
					api.send_message(sender, message.get_message())
			elif 'attachments' in event['message'] and 'payload' in event['message']['attachments'][0] and 'coordinates' in event['message']['attachments'][0]['payload']:
				lat = str(event['message']['attachments'][0]['payload']['coordinates']['lat'])
				long = str(event['message']['attachments'][0]['payload']['coordinates']['long'])
				url = "https://www.google.rs/maps/search/Telenor/@" + lat + "," + long + ",15.5z"
				message = UrlButton(url, "Otvori mapu")
				api.send_message(sender, message.get_standalone_button("Najbliže radnje su pronađene."))
			else:
				message = TextMessage("Primljena je poruka bez teksta ili lokacije, možete li ponovo objasniti?")
				api.send_message(sender, message.get_message())
		else:
			message = TextMessage("Nepravilan oblik poruke je primljen, možete li ponovo objasniti?")
			api.send_message(sender, message.get_message())
		api.set_typing_off(sender)
		
    return ''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
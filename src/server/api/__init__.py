# coding: UTF-8

import config
import requests
from templates.list import *
from templates.button import *

BASE_URL = 'https://graph.facebook.com/v2.6/me/'
MESSAGES_URL = BASE_URL + "messages"
THREAD_SETTINGS_URL = BASE_URL + "thread_settings"
ACCESS_TOKEN = config.ACCESS_TOKEN


def send_url(app, to_user):
    message = ListMessage(False)
    urlButton1 = UrlButton(
        url="https://www.telenor.rs/webshop/sr/Privatni-korisnici/Mobilni-telefoni/Apple/iPhone_6_64GB_Space_Grey/",
        title="Pogledaj telefon")
    postbackButton1 = PostbackButton(
        payload=config.PAYLOAD_PHONE_PRICE + "IPHONE_6",
        title="Cena telefona"
    )
    urlButton2 = UrlButton(
        url="https://www.telenor.rs/webshop/sr/Privatni-korisnici/Mobilni-telefoni/Apple/iPhone_6_64GB_Space_Grey/",
        title="Pogledaj telefon")
    postbackButton2 = PostbackButton(
        payload=config.PAYLOAD_PHONE_PRICE + "GALAXY_S7",
        title="Cena telefona"
    )

    message.add_element(
        title="APPLE IPHONE 6 64GB SPACE GREY",
        image_url="https://www.telenor.rs/media/eshop/phones/phone_720_21.jpg",
        subtitle="Retina HD display, iOS 8.0.2, A8 cip, 64GB, M8 koprocesor za obradu pokreta...",
        url="https://www.telenor.rs/webshop/sr/Privatni-korisnici/Mobilni-telefoni/Apple/iPhone_6_64GB_Space_Grey/",
        buttons=[urlButton1.get_button(), postbackButton1.get_button()])
    message.add_element(
        title="SAMSUNG GALAXY S7",
        image_url="https://www.telenor.rs/media/eshop/phones/phone_846_21.jpg",
        subtitle="Quad-core 4 x 2.3GHz + 4 x 1.6GHz (Exynos 8890), 4GB RAM, 12 Mpix kamera, 4G...",
        url="https://www.telenor.rs/webshop/sr/Privatni-korisnici/Mobilni-telefoni/Apple/iPhone_6_64GB_Space_Grey/",
        buttons=[urlButton2.get_button(), postbackButton2.get_button()])

    if app is not None:
        app.logger.debug(message.get_message())
    send_message(to_user, message.get_message())


def send_message(to_user, message):
    data = {
        'recipient': {
            'id': to_user
        },
        'message': message
    }
    r = requests.post(MESSAGES_URL, params={'access_token': ACCESS_TOKEN}, json=data)


def sender_action(user, action):
    typing = {
        'recipient': {
            'id': user
        },
        'sender_action': action
    }
    r = requests.post(MESSAGES_URL, params={'access_token': ACCESS_TOKEN}, json=typing)


def message_seen(user):
    sender_action(user, 'mark_seen')


def set_typing_on(to_user):
    sender_action(to_user, 'typing_on')
	
def set_typing_off(to_user):
    sender_action(to_user, 'typing_off')

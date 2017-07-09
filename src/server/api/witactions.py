# coding: UTF-8

import api
import config
from templates.text import *
from templates.button import CallButton, QuickReply


class BadQuestion(Exception):
    pass


def send(request, response):
    """
    Ovde vidimo da li je neka akcija setovala err,
     ako nema err uopšte, onda nijedna nije ni pozvana
     u svakom slučaju, ne znamo da odgovorimo
    """
    if ('err' not in request['context']) or request['context']['err']:
        message = TextMessage("Ne razumem Vas, možete li ponovo objasniti?")
        api.send_message(request['session_id'], message.get_message())


def get_tarifa(request):
    context = {"err": False}
    try:
        validate_request(request, 'tarifa', ['tarifa'])
        # Paralelno inforamcije za vise tarifa
        tarife = [tarifa['value'] for tarifa in request['entities']['tarifa']]
        message = TextMessage("Kostaju mnogo, puno, puno ti vasi paketi: " + ", ".join(tarife))
        api.send_message(request['session_id'], message.get_message())
        context["err"] = False
    except BadQuestion:
        context['err'] = True
    return context


def get_price(request):
    context = {"err": False}
    try:
        validate_request(request, 'phone_price', ['phone'])  # proverimo da li je za ovu akciju
        phones = [phone['value'] for phone in request['entities']['phone']]
        message = TextMessage("Interesantan izbor teleona: " + ", ".join(phones))
        api.send_message(request['session_id'], message.get_message())
        api.send_url(None, request['session_id'])
    except BadQuestion:
        context['err'] = True  # ovaj zahtev nije za ovu akciju
    return context
	
	
def greeting(request):
	context = {"err": False}
	try:
		validate_request(request, 'greeting')
		message = QuickReply("Dobar dan poštovani, kako mogu da Vam pomognem?")
		message.addButton("Kako da počnem?", config.PAYLOAD_SHOW_HELP)
		api.send_message(request['session_id'], message.get_button())
	except BadQuestion:
		context['err'] = True  # ovaj zahtev nije za ovu akciju
	return context
	

def get_podrska(request):
	context = {"err": False}
	try:
		validate_request(request, 'podrska')
		message = CallButton(
			"Poštovani, korisničku podršku možete dobiti na broj telefona " + config.TELENOR_SUPPORT_PHONE_NUMBER + ".",
			"Pozovite odmah",
			config.TELENOR_SUPPORT_PHONE_NUMBER)
		api.send_message(request['session_id'], message.get_button())
	except BadQuestion:
		context['err'] = True  # ovaj zahtev nije za ovu akciju
	return context
	
	
def get_ekspoziture(request):
	context = {"err": False}
	try:
		validate_request(request, 'ekspoziture')
		message = QuickReply("Poštovani, kako bi smo Vam našli najbliže prodajno mesto, molimo podelite Vašu lokaciju klikom na dugme.")
		message.addLocation()
		api.send_message(request['session_id'], message.get_button())
	except BadQuestion:
		context['err'] = True  # ovaj zahtev nije za ovu akciju
	return context


def validate_request(request, intent, required_entities=[], min_confidence=0.5):
    """
        u nekim slučajevima, kad ne zna šta će
        wit, izgleda, iskoristi random akciju
        ovo služi da proveri da li je akciji stigao
        zahtev koji je stvarno za nju
    """
    entities = request['entities']
    if ('intent' not in entities) or (entities['intent'][0]['value'] != intent) \
            or (entities['intent'][0]['confidence'] < min_confidence):
        raise BadQuestion()
    for entity in required_entities:
        if entity not in entities or len(entities[entity]) == 0:
            raise BadQuestion()


"""
    mapa akcija na funkcije
    akcije se definišu u delu stories
    na sajtu
"""
actions = {
    'send': send,
    'getTarifa': get_tarifa,
    'getPrice': get_price,
	'greeting': greeting,
	'callPodrska': get_podrska,
	'getEkspoziture': get_ekspoziture
}

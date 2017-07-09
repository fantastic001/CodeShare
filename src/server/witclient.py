# coding: UTF-8

from config import WIT_AI_ACCESS_TOKEN
from wit import Wit
from .witactions import actions

client = Wit(access_token=WIT_AI_ACCESS_TOKEN, actions=actions)

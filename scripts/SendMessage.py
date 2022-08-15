import discord

# webhook for nepse discord general
# https://discord.com/api/webhooks/987378652813623367/splN2-ePyKsx4UM2BY11jKNIhMh7MABEBdPpaEjQX_RLeEmZM5ya7o1ed_IkFYhBBh3o
import requests
from discord import Webhook, RequestsWebhookAdapter


webhook_url = "https://discord.com/api/webhooks/987378652813623367/splN2-ePyKsx4UM2BY11jKNIhMh7MABEBdPpaEjQX_RLeEmZM5ya7o1ed_IkFYhBBh3o"

url_Stochastic_RSI_webhook = "https://discord.com/api/webhooks/1008748730494763130/PdaWZK6AS8xb3zUDjTm66fAnOw5jjXOx8EvHvJ7ZfSzZhxhdTv965K3qaDwONJYwc91q"
url_Bollinger_Band_webhook = "https://discord.com/api/webhooks/1008748991804080278/GAn9cfQemeWLzLJTh3LgkJIZHG4OyKS9ccageEauCsykrSMzt0uqpbLKiKl2qPl1FJe9"

webhook = Webhook.from_url(webhook_url, adapter=RequestsWebhookAdapter())
# webhook.send("Hello World")


def send_BollingerBand_message(buylist, selllist):
    message = 'Today\'s Bollinger Band Analysis\n\n'
    message += 'BUY LIST --> Stocks deviating upward from lower band\n'
    for b in buylist:
        message += b+'\n'

    message += '\nSell LIST --> Stocks deviating downward from upper band\n'
    for s in selllist:
        message += s+'\n'
    webhook = Webhook.from_url(url_Bollinger_Band_webhook, adapter=RequestsWebhookAdapter())
    webhook.send(str(message))


def send_StochasticRSI_message(buylist, selllist):
    message = 'Today\'s Stochastic RSI Analysis\n\n'
    message += 'Bullish Crossover at the bottom Scripts good to BUY\n'
    for b in buylist:
        message += b+'\n'

    message += '\nBearish Crossover at the top Scripts good to SELL\n'
    for s in selllist:
        message += s+'\n'
    webhook = Webhook.from_url(url_Stochastic_RSI_webhook, adapter=RequestsWebhookAdapter())
    webhook.send(str(message))

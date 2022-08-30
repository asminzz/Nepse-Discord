import discord
from discord import Webhook, RequestsWebhookAdapter
import os

webhook_url = os.environ['WEBHOOK_URL']
url_Stochastic_RSI_webhook = os.environ['WEBHOOK_STOCHASTIC_RSI ']
url_Bollinger_Band_webhook = os.environ['WEBHOOK_BOLLINGER_BAND ']


webhook = Webhook.from_url(webhook_url, adapter=RequestsWebhookAdapter())


def send_BollingerBand_message(buylist, selllist):
    message = 'Today\'s Bollinger Band Analysis\n\n'
    message += 'BUY LIST --> Stocks that touched the lower band --> Watch for next buy\n'
    for b in buylist:
        message += b+'\n'

    message += '\nSell LIST --> Stocks that touched the upper band --> Watch for sell\n'
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

import hmac
import hashlib
import base64
import binascii
import urllib
import json
from flask import Blueprint, render_template, request

from plugins.inboundwebhook.models import trigger

import jimi

pluginPages = Blueprint('inboundwebhookPages', __name__)

@pluginPages.route("/public/<token>/",methods=["GET","POST"])
def __PUBLIC__inboundwebhook(token):
    webhook = trigger._inboundwebhook().getAsClass(query={ "token" : token })[0]
    if webhook.enabled and webhook.authenticated == False:
        if request.method == 'POST':
            events = json.loads(jimi.api.request.data)
        else:
            events = webhook.customEvents
        maxDuration = 0
        if webhook.maxDuration > 0:
            maxDuration = webhook.maxDuration
        jimi.workers.workers.new("inboundwebhookpublic{0}".format(webhook._id),webhook.notify,(events,),maxDuration=maxDuration)
        return { }, 200
    return { }, 404

@pluginPages.route("/<token>/",methods=["GET","POST"])
def inboundwebhook(token):
    webhook = trigger._inboundwebhook().getAsClass(sessionData=jimi.api.g.sessionData,query={ "token" : token })[0]
    if webhook.enabled and webhook.authenticated == True:
        if request.method == 'POST':
            events = json.loads(jimi.api.request.data)
        else:
            events = webhook.customEvents
        maxDuration = 0
        if webhook.maxDuration > 0:
            maxDuration = webhook.maxDuration
        jimi.workers.workers.new("inboundwebhookpublic{0}".format(webhook._id),webhook.notify,(events,),maxDuration=maxDuration)
        return { }, 200
    return { }, 404
    
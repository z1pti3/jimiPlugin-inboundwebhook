import json
import urllib
import requests
from flask import Blueprint, render_template, request

from plugins.inboundwebhook.models import trigger

import jimi

pluginPages = Blueprint('inboundwebhookPages', __name__)

@pluginPages.route("/public/<token>/",methods=["GET","POST"])
def __PUBLIC__inboundwebhook(token):
    webhook = trigger._inboundwebhook().getAsClass(query={ "token" : token })[0]
    if webhook.enabled and webhook.authenticated == False:
        apiEndpoint = "inboundwebhook/public/{0}/".format(token)
        url = jimi.cluster.getMaster()
        systemSessionToken = jimi.auth.generateSystemSession()
        headers = { "x-api-token" : systemSessionToken}
        if request.method == 'POST':
            response = requests.post("{0}/{1}/{2}".format(url,"plugin",apiEndpoint), headers=headers, data= jimi.api.request.data, timeout=60)
        else:
            response = requests.get("{0}/{1}/{2}".format(url,"plugin",apiEndpoint), headers=headers, timeout=60)
        if response.status_code == 200:
            return { }, 200
    return { }, 404

@pluginPages.route("/<token>/",methods=["GET","POST"])
def inboundwebhook(token):
    webhook = trigger._inboundwebhook().getAsClass(sessionData=jimi.api.g.sessionData,query={ "token" : token })[0]
    if webhook.enabled and webhook.authenticated == True:
        apiEndpoint = "inboundwebhook/{0}/".format(token)
        url = jimi.cluster.getMaster()
        headers = { "x-api-token" : jimi.api.g.sessionToken }
        if request.method == 'POST':
            response = requests.post("{0}/{1}/{2}".format(url,"plugin",apiEndpoint), headers=headers, data= jimi.api.request.data, timeout=60)
        else:
            response = requests.get("{0}/{1}/{2}".format(url,"plugin",apiEndpoint), headers=headers, timeout=60)
        if response.status_code == 200:
            return { }, 200
    return { }, 404
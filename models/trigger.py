import secrets

import jimi

class _inboundwebhook(jimi.trigger._trigger):
    token = str()
    authenticated = bool()
    customEvents = list()

    def setAttribute(self,attr,value,sessionData=None):
        if attr == "token":
            self.token = secrets.token_hex(128)
            self.update(['token'])
            return True
        return super(_inboundwebhook, self).setAttribute(attr,value,sessionData)
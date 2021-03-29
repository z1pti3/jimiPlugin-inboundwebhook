from core import plugin, model

class _inboundwebhook(plugin._plugin):
    version = 0.1

    def install(self):
        # Register models
        model.registerModel("inboundwebhook","_inboundwebhook","_trigger","plugins.inboundwebhook.models.trigger")
        return True

    def uninstall(self):
        # deregister models
        model.registerModel("inboundwebhook","_inboundwebhook","_trigger","plugins.inboundwebhook.models.trigger")
        return True

    def upgrade(self,LatestPluginVersion):
        pass

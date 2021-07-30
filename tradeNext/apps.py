from django.apps import AppConfig

class tradeNextConfig(AppConfig):
    name = 'tradeNext'

    def ready(self):
        
        from shareUpdater import updater
        updater.start()
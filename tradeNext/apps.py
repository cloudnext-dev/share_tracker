from django.apps import AppConfig
class tradeNextConfig(AppConfig):
	name = 'tradeNext'
	def ready(self):
		from maintenance_mode.core import get_maintenance_mode, set_maintenance_mode
		set_maintenance_mode(False)
		from shareUpdater import updater
		updater.start()
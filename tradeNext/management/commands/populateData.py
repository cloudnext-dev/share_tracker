from tradeNext.models import Customer, Broker, Account, Strategy, Trades, Reporting, AssetDetails
import csv
from django.core.management.base import BaseCommand, CommandError
from yahoo_fin import stock_info as si
import random

class Command(BaseCommand):
	help = 'Refesh Stock Pricee In Every 30(Mins)'
	def handle(self, *args, **options):
		try:
			acc = Account.objects.get(AccountId = 4)
			st4 = Strategy.objects.get(StrategyId = 4)
			st3 = Strategy.objects.get(StrategyId = 3)
			st2 = Strategy.objects.get(StrategyId = 2)
			asset_csv = open('tradeNext/Book1.csv', 'r', encoding = "utf-8")
			reader = csv.reader(asset_csv)
			headers = next(reader, None)[1:]
			for row in reader:
				asset_dict = {}
				asset_dict['AssetId'] = row[0]
				asset_dict['AccountId'] = acc
				asset_dict['StrategyId'] = random.choice([st4, st3, st2])
				asset_dict['EntryPrice'] = float(row[3])
				try:
					assetInfo = AssetDetails.objects.create(**asset_dict)
					print(assetInfo)
				except:
					pass
		except:
			self.stdout.write(self.style.ERROR('Field "AssetId" does not exist.'))
			return
		self.stdout.write(self.style.SUCCESS('Successfully Updated all Asset Price'))
		return
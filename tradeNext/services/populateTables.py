from tradeNext.models import Customer, Broker, Account, Strategy, Trades, Reporting, AssetDetails
import csv
import os
from django.core.files.storage import FileSystemStorage
import concurrent.futures
import configparser
config = configparser.ConfigParser()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(BASE_DIR, os.pardir))
configFile = os.path.join(BASE_DIR, 'config.ini')
config.read(configFile)
class populateTables():
	def insertAssetsDetails(self, filename, strategy, account):
		fs = FileSystemStorage()
		filePath = os.path.join(fs.location, filename)
		asset_csv = open(filePath, 'r', encoding = "utf-8")
		reader = csv.reader(asset_csv)
		headers = next(reader, None)[1:]
		AssetDetails.objects.filter(AccountId = account.AccountId).delete()
		insertedList = []
		notInsertedList = []
		argList = []
		resultDict = {}
		for row in reader:
			asset_dict = {}
			asset_dict['AssetId'] = row[0]
			asset_dict['AccountId'] = account
			asset_dict['StrategyId'] = strategy
			asset_dict['EntryPrice'] = float(row[1])
			argList.append(asset_dict)
		with concurrent.futures.ThreadPoolExecutor(max_workers=int(config["ConcurrentProcess"]["Number"])) as executor:
			result_futures = executor.map(lambda f: AssetDetails.objects.create(**f), argList)
			inserted = []
			failed = []
		
		for future in result_futures:
			try:
				inserted.append((future.AssetId, future.EntryPrice))
			except:
				failed.append((future.AssetId, future.EntryPrice))
				pass
		
		resultDict['success'] = inserted
		resultDict['failed'] = failed
		result = "Inserted Values in Database"
		return resultDict
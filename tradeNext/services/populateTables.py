from tradeNext.models import Customer, Broker, Account, Strategy, Trades, Reporting, AssetDetails
import csv
import os
from django.core.files.storage import FileSystemStorage
import concurrent.futures
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
		for row in reader:
			asset_dict = {}
			asset_dict['AssetId'] = row[0]
			asset_dict['AccountId'] = account
			asset_dict['StrategyId'] = strategy
			asset_dict['EntryPrice'] = float(row[1])
			argList.append(asset_dict)
		#results = []
		with concurrent.futures.ThreadPoolExecutor(max_workers=120) as executor:
			executor.map(lambda f: AssetDetails.objects.create(**f), argList)

		result = "Inserted Values in Database"
		#insertedIndex = []	
		#for result in results:
		#	print('Hello------------------------>',result)
		#	insertedIndex.append(result.__next__().id)
		#print(insertedIndex)
		"""
		try:
			assetInfo = AssetDetails.objects.create(**asset_dict)
			insertedList.append(row[0])
			print('Successfully Inserted --->',assetInfo)
		except:
			print('Failed to Insert--->',row[0])
			notInsertedList.append(row[0])
			pass
		"""
		#return {'inserted': insertedList, 'notInserted': notInsertedList}
		return result
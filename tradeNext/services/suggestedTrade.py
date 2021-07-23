from tradeNext.models import Customer, Broker, Account, Strategy, Trades, Reporting, AssetDetails
from itertools import chain
class suggestedTrade():
	def __init__(self):
		sectors = AssetDetails.objects.exclude(Sector__isnull=True).\
			exclude(Sector__exact='').order_by('Sector').values_list('Sector').distinct()
		self.sectors = [i[0] for i in list(sectors)]
		strategies = AssetDetails.objects.all().order_by('StrategyId').values_list('StrategyId').distinct()
		self.strategies = [i[0] for i in list(strategies)]
		self.industry = ''

	def allSuggestedTrade(self):	
		strategyWiseList = AssetDetails.objects.none()
		for strategy in self.strategies:
			sectorWiseList = AssetDetails.objects.none()
			stInfo = Strategy.objects.get(StrategyId = strategy)
			for sector in self.sectors:
				queryList = AssetDetails.objects.all()
				queryList = queryList.filter(Sector = sector, StrategyId = strategy).order_by("EntryPriceDiff")
				if len(queryList) >= stInfo.maxTradePerSector:
					queryList = queryList.filter(Sector = sector, StrategyId = strategy).order_by("EntryPriceDiff")[:stInfo.maxTradePerSector]
				else:
					queryList = queryList.filter(Sector = sector, StrategyId = strategy).order_by("EntryPriceDiff")
				if len(self.sectors) >= stInfo.maxTradePerDay:
					sectorWiseList = list(chain(sectorWiseList, queryList[:1]))
				else:
					sectorWiseList = list(chain(sectorWiseList, queryList))
			sectorWiseList = sorted(sectorWiseList,key=lambda asset: asset.EntryPriceDiff)
			sectorWiseList = sectorWiseList[:stInfo.maxTradePerDay]
			strategyWiseList = list(chain(strategyWiseList, sectorWiseList))
		strategyWiseList = sorted(strategyWiseList,key=lambda asset: asset.EntryPriceDiff)
		return strategyWiseList

	def sectorOnlySuggestTrade(self, sector):
		strategyWiseList = self.allSuggestedTrade()
		strategyWiseList = list(filter(lambda asset: asset.Sector == sector, strategyWiseList))
		return strategyWiseList
	def industryOnlySuggestTrade(self, industry):
		strategyWiseList = self.allSuggestedTrade()
		strategyWiseList = list(filter(lambda asset: asset.Industry == industry, strategyWiseList))
		return strategyWiseList

	def secIndSuggestTrade(self, sector, industry):
		strategyWiseList = self.allSuggestedTrade()
		strategyWiseList = list(filter(lambda asset: asset.Sector == sector, strategyWiseList))
		strategyWiseList = list(filter(lambda asset: asset.Industry == industry, strategyWiseList))
		return strategyWiseList
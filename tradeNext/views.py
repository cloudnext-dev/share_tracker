from django.shortcuts import render
from django.http import HttpResponse
from .models import Customer, Broker, Account, Strategy, Trades, Reporting, AssetDetails
from django.http import JsonResponse
from rest_framework.generics import ListAPIView
from tradeNext.serializers.assetDetailsSerializers import AssetDetailsSerializers
from tradeNext.services import suggestedTrade, populateTables
from django.core.files.storage import FileSystemStorage
from maintenance_mode.decorators import force_maintenance_mode_off, force_maintenance_mode_on
from maintenance_mode.core import get_maintenance_mode, set_maintenance_mode
from datetime import datetime
import concurrent.futures


def Index(request):
	return render(request, 'index.html')

def limitTrade(request):
	return render(request, "limitTrade.html", {})

class AssetListing(ListAPIView):
	serializer_class = AssetDetailsSerializers

	def get_queryset(self):
		queryList = AssetDetails.objects.all()
		sector = self.request.query_params.get('sector', None)
		industry = self.request.query_params.get('industry', None)
		sort_by = self.request.query_params.get('sort_by', None)
		if sector:
			queryList = queryList.filter(Sector = sector)

		if industry:
			queryList = queryList.filter(Industry = industry)

		if sector and industry:
			queryList = queryList.filter(Sector = sector, Industry = industry)		
		
		if sort_by == "EntryPriceDiff":
		    queryList = queryList.order_by("EntryPriceDiff")
		elif sort_by == "Avg1Diff":
		    queryList = queryList.order_by("Avg1Diff")
		elif sort_by == "Avg2Diff":
			queryList = queryList.order_by("Avg2Diff")

		return queryList

def suggestLimitTrade(request):
	return render(request, "suggestedLimitTrade.html", {})

class SuggestedAssetListing(ListAPIView):
	serializer_class = AssetDetailsSerializers

	def get_queryset(self):
		suggestedTradeObj = suggestedTrade.suggestedTrade()
		strategyWiseList = suggestedTradeObj.allSuggestedTrade()
		sector = self.request.query_params.get('sector', None)
		industry = self.request.query_params.get('industry', None)
		sort_by = self.request.query_params.get('sort_by', None)
		if sector:
			strategyWiseList = suggestedTradeObj.sectorOnlySuggestTrade(sector)
		if industry:
			strategyWiseList = suggestedTradeObj.industryOnlySuggestTrade(industry)
		if sector and industry:
			strategyWiseList = suggestedTradeObj.secIndSuggestTrade(sector, industry)
		
		return strategyWiseList


def getSectors(request):
    if request.method == "GET" and request.is_ajax():
        sectors = AssetDetails.objects.exclude(Sector__isnull=True).\
            exclude(Sector__exact='').order_by('Sector').values_list('Sector').distinct()
        sectors = [i[0] for i in list(sectors)]
        data = {
            "sectors": sectors, 
        }
        return JsonResponse(data, status = 200)


def getIndustry(request):
    if request.method == "GET" and request.is_ajax():
        industries = AssetDetails.objects.exclude(Industry__isnull=True).\
        	exclude(Industry__exact='').order_by('Industry').values_list('Industry').distinct()
        industries = [i[0] for i in list(industries)]
        data = {
            "industries": industries, 
        }
        return JsonResponse(data, status = 200)

def refreshStocks(request):
	if request.method == "GET" and request.is_ajax():
		from shareUpdater import updater
		updater.update_stock()
		data = {
            "status": True, 
        }
		return JsonResponse(data, status = 200)        

@force_maintenance_mode_off
def getAccounts(request):
    if request.method == "GET" and request.is_ajax():
        accounts = Account.objects.all().order_by('AccountName').values_list('AccountName').distinct()
        accounts = [i[0] for i in list(accounts)]
        data = {
            "accounts": accounts, 
        }
        return JsonResponse(data, status = 200)
@force_maintenance_mode_off
def getStrategy(request):
    if request.method == "GET" and request.is_ajax():
        strategies = Strategy.objects.exclude(StrategyName__isnull=True).\
        	exclude(StrategyName__exact='').order_by('StrategyName').values_list('StrategyName').distinct()
        strategies = [i[0] for i in list(strategies)]
        data = {
            "strategies": strategies, 
        }
        return JsonResponse(data, status = 200)
@force_maintenance_mode_off
def uploadAssets(request):
	if request.method == 'POST' and request.FILES.get('assetFile') and request.FILES.get('assetFile').content_type == 'application/vnd.ms-excel':
		assetFile = request.FILES['assetFile']
		#brokerAccountId = request.POST.get('brokers')
		#brokerObj = Broker.objects.get(BrokerAccountId = brokerAccountId)
		accountName = request.POST.get('accounts')
		accountObj = Account.objects.get(AccountName = accountName)
		strategyName = request.POST.get('strategies')
		strategyObj = Strategy.objects.get(StrategyName = strategyName)
		fs = FileSystemStorage()
		updateFileName = assetFile.name.split('.')
		date = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
		updateFileName = updateFileName[0] + '_' + date + '.' + updateFileName[1]
		filename = fs.save(updateFileName, assetFile)
		uploaded_file_url = fs.url(filename)
		populateModel = populateTables.populateTables()
		set_maintenance_mode(True)
		insertionResult = populateModel.insertAssetsDetails(filename, strategyObj, accountObj)
		set_maintenance_mode(False)
		return render(request, 'uploadAssets.html', {
			'result': insertionResult
		})
	return render(request, 'uploadAssets.html', {
			'result': 'No File Selected / Csv File Only'
		})


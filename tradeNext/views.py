from django.shortcuts import render
from django.http import HttpResponse
from .models import Customer, Broker, Account, Strategy, Trades, Reporting, AssetDetails
from django.http import JsonResponse
from rest_framework.generics import ListAPIView
from .serializers import AssetDetailsSerializers
from tradeNext.services import suggestedTrade


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




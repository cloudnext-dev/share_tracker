from django.urls import path

from . import views

from tradeNext.views import *

urlpatterns = [
	path('', Index, name = "index"),
	path('limitTrade/', limitTrade, name = 'limitTrade'),
    path("asset_listing/", AssetListing.as_view(), name = 'listing'),
    path('suggestLimitTrade/', suggestLimitTrade, name = 'suggestLimitTrade'),
    path("suggest_listing/", SuggestedAssetListing.as_view(), name = 'suggestlisting'),
    path("ajax/sectors/", getSectors, name = 'get_sectors'),
    path("ajax/industries/", getIndustry, name = 'get_industry'),
    path("ajax/brokers/", getBrokers, name = 'get_brokers'),
    path("ajax/strategies/", getStrategy, name = 'get_strategy'),
    path("uploadAssets/", uploadAssets, name = 'uploadAssetFile')
]
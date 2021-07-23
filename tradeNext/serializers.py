from rest_framework import serializers
from .models import AssetDetails, Strategy

class AssetDetailsSerializers(serializers.ModelSerializer):
	StrategyId = serializers.CharField(source='StrategyId.StrategyName')
	AccountId = serializers.CharField(source='AccountId.BrokerId.BrokerAccountId')
	class Meta:
	    model = AssetDetails
	    fields = ('AssetId', 'AccountId', 'StrategyId', 'EntryPrice', 'AvgEntryPoint1', 'AvgEntryPoint2', 'TargetPrice', 'Sector', 'Industry', 'Beta', 'NextEarningDate', 'CurrentMarketPrice', 'EntryPriceDiff', 'Avg1Diff', 'Avg2Diff', 'Quantity')
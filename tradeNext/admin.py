from django.contrib import admin
from .models import Customer, Broker, Account, Strategy, Trades, Reporting, AssetDetails

class CustomerAdmin(admin.ModelAdmin):
	list_display = ('FirstName', 'LastName', 'EmailId', 'Mobile')
	list_filter = ("FirstName", )
	search_fields = ("EmailId", "FirstName")

class BrokerAdmin(admin.ModelAdmin):
	list_display = ('BrokerId', 'BrokerName', 'BrokerAccountId')
	list_filter = ("BrokerName", )
	search_fields = ("BrokerName",)

class AccountAdmin(admin.ModelAdmin):
	list_display = ('AccountId', 'BrokerId', 'ConnectionStatus', 'SpendLimit', 'AccountName')
	list_filter = ("AccountId", 'BrokerId','SpendLimit')
	search_fields = ("SpendLimit",)	

class StrategyAdmin(admin.ModelAdmin):
	list_display = ('StrategyId', 'StrategyName', 'StrategyType', 'MaxInvestment', 'TargetPrice', 'AvgPoint1', 'AvgPoint2', 'TotalFundAllocated')

class AssetDetailsAdmin(admin.ModelAdmin):
	list_display = ('AssetId', 'AccountId', 'StrategyId', 'EntryPrice', 'AvgEntryPoint1', 'AvgEntryPoint2', 'TargetPrice', 'Sector', 'Industry', 'Beta', 'NextEarningDate', 'CurrentMarketPrice', 'EntryPriceDiff', 'Avg1Diff', 'Avg2Diff', 'Quantity', 'LastUpdatedOn')
	readonly_fields = ('AvgEntryPoint1', 'AvgEntryPoint2', 'TargetPrice', 'Sector', 'Industry', 'NextEarningDate', 'EntryPriceDiff', 'Avg1Diff', 'Avg2Diff', 'Quantity', 'LastUpdatedOn')

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Broker, BrokerAdmin)
admin.site.register(Account, AccountAdmin)
#admin.site.register(Strategy, StrategyAdmin)
admin.site.register(Strategy)
admin.site.register(AssetDetails, AssetDetailsAdmin)
admin.site.register(Trades)
admin.site.register(Reporting)
admin.site.site_header = "TradeNext Admin Panel"
#tradersync

# Register your models here.

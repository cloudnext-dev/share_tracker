from django.db import models
from decimal import Decimal
import yfinance as yf
from yahoo_fin import stock_info as si
from datetime import datetime
from tradeNext.services import parseStock

class Customer(models.Model):
    UserId = models.AutoField(primary_key=True)
    FirstName = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100)
    EmailId =  models.EmailField(max_length=100)
    Mobile = models.IntegerField()

    class Meta:
        verbose_name = 'Customer'

    def __str__(self):
        return "%s %s" % (self.FirstName, self.LastName)

class Broker(models.Model):
	BrokerId = models.AutoField(primary_key=True)
	BrokerName = models.CharField(max_length=50)
	BrokerAccountId = models.CharField(max_length=100)

	class Meta:
		verbose_name = 'Broker'

	def __str__(self):
		return "%s" % (self.BrokerAccountId)

class Account(models.Model):
	AccountId = models.AutoField(primary_key=True)
	AccountName = models.CharField(max_length=50, default='Hello')
	UserId = models.ForeignKey(Customer, on_delete=models.CASCADE)
	BrokerId = models.ForeignKey(Broker, on_delete=models.CASCADE)
	ConnectionStatus = models.BooleanField(default=False)
	SpendLimit = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal(0.00))

	class Meta:
		verbose_name = 'Account'
	def __str__(self):
		return "%s" % (self.BrokerId)

class Strategy(models.Model):
	StrategyId = models.AutoField(primary_key=True)
	StrategyName = models.CharField(max_length=15)
	StrategyType = models.IntegerField(choices=[(1, 'Limit Trade'), (2, 'Auto Trade'), (3, 'Direct Trade')]) 
	MaxInvestment = models.FloatField()
	TargetPrice = models.FloatField()
	AvgPoint1 = models.FloatField()
	AvgPoint2 = models.FloatField()
	maxTradePerDay = models.IntegerField(default=0)
	maxTradePerSector = models.IntegerField(default=0)
	TotalFundAllocated = models.FloatField()
    
	class Meta:
		verbose_name = 'Strategy'

	def __str__(self):
		return "%s" % (self.StrategyName)

class AssetDetails(models.Model):
	AssetId = models.CharField(max_length=15)
	AccountId = models.ForeignKey(Account, on_delete=models.CASCADE)
	StrategyId = models.ForeignKey(Strategy, on_delete=models.CASCADE)
	EntryPrice = models.FloatField()
	CurrentMarketPrice = models.FloatField(default=Decimal(0.00))
	EntryPriceDiff = models.FloatField(default=Decimal(0.00))
	AvgEntryPoint1= models.FloatField(default=Decimal(0.00))
	Avg1Diff = models.FloatField(default=Decimal(0.00))
	AvgEntryPoint2 = models.FloatField(default=Decimal(0.00))
	Avg2Diff = models.FloatField(default=Decimal(0.00))
	TargetPrice = models.FloatField(default=Decimal(0.00))
	Quantity = models.IntegerField(default=0)
	Sector = models.CharField(max_length=50)
	Industry = models.CharField(max_length=50)
	Beta = models.FloatField(default=Decimal(0.00))
	NextEarningDate = models.DateTimeField(null=True, blank=True)
	LastUpdatedOn = models.DateTimeField(default=datetime.now, blank=True)

	class Meta:
		verbose_name = 'AssetDetails'


	def _percent_diff(self, Price2, Price1):
		return (Price2 - Price1) / Price1 * 100.0 if Price1 != 0 else float("inf") * abs(Price2) / Price2 if Price2 != 0 else 0.0

	def save(self, *args, **kwargs):
		stInfo = Strategy.objects.get(StrategyName=self.StrategyId)
		#self.CurrentMarketPrice = si.get_live_price(self.AssetId)
		stockInfo = parseStock.parseStock(self.AssetId, 'price')
		stockPrice = stockInfo.get_price()
		if ',' in stockPrice:
			stockPrice = stockPrice.replace(',', '')
		self.CurrentMarketPrice = float(stockPrice)
		if NextEarningDate and not self.NextEarningDate:
			try:
				NextEarningDate = stockInfo.get_earning_date() 
				NextEarningDate = NextEarningDate.replace(',', '')
				print('NextEarningDate', NextEarningDate)
				self.NextEarningDate = datetime.strptime(NextEarningDate, '%b %d %Y')
				#self.NextEarningDate = si.get_next_earnings_date(self.AssetId)
			except:
				pass
		self.AvgEntryPoint1 = self.EntryPrice - (self.EntryPrice*stInfo.AvgPoint1/100)
		self.AvgEntryPoint2 = self.AvgEntryPoint1 - (self.AvgEntryPoint1*stInfo.AvgPoint2/100)
		self.TargetPrice = self.EntryPrice + (self.EntryPrice*stInfo.TargetPrice/100)
		if not self.Sector and not self.Industry:
			#stockInfo = yf.Ticker(self.AssetId)
			stockInfo = parseStock.parseStock(self.AssetId, 'other')
			self.Sector = stockInfo.get_sector()
			self.Industry = stockInfo.get_industry()
			#self.Sector = stockInfo.info.get('sector', 'N/a')
			#self.Industry = stockInfo.info.get('industry', 'N/a')
		self.EntryPriceDiff = self._percent_diff(self.CurrentMarketPrice, self.EntryPrice)
		self.Avg1Diff = self._percent_diff(self.CurrentMarketPrice, self.AvgEntryPoint1)
		self.Avg2Diff = self._percent_diff(self.CurrentMarketPrice, self.AvgEntryPoint2)
		minQuantity = int(stInfo.MaxInvestment/self.CurrentMarketPrice)
		maxQuantity = int(stInfo.MaxInvestment/self.CurrentMarketPrice) + 1
		minInvestment = minQuantity*self.CurrentMarketPrice
		maxInvestment = maxQuantity*self.CurrentMarketPrice
		if minInvestment < stInfo.MaxInvestment:
			self.Quantity = minQuantity
		else:
			self.Quantity = maxQuantity
		self.LastUpdatedOn = datetime.now()
		super(AssetDetails, self).save(*args, **kwargs)
	

class Trades(models.Model):
	TradeId = models.AutoField(primary_key=True)
	UserId = models.ForeignKey(Customer, on_delete=models.CASCADE)
	AssetId = models.ForeignKey(AssetDetails, on_delete=models.CASCADE)
	StrategyId = models.ForeignKey(Strategy, on_delete=models.CASCADE)
	AccountId = models.ForeignKey(Account, on_delete=models.CASCADE)
	StartDate = models.DateTimeField()
	EndDate = models.DateTimeField()
	AssetPriceAEntry = models.FloatField()
	AssetPriceAtClose = models.FloatField()
	Quantity = models.IntegerField()
	Status = models.IntegerField()
	MBP = models.FloatField()
	CBP = models.FloatField()
	Commissions = models.FloatField()
	AvgDate1 = models.DateTimeField()
	AvgDate2 = models.DateTimeField()
	AvgDate3 = models.DateTimeField()
	TradeAverage = models.BooleanField()

	class Meta:
		verbose_name = 'Trade'

class Reporting(models.Model):
	RealizePL = models.FloatField()
	RealizedPLPercent = models.FloatField()
	UnRealizedPL = models.FloatField()
	RealizedPLPercent = models.FloatField()
	DaysInTrade = models.IntegerField()

	class Meta:
		verbose_name = 'Reporting'
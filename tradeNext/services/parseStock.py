import requests
from lxml import html
import random
import os
import configparser
config = configparser.ConfigParser()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(BASE_DIR, os.pardir))
configFile = os.path.join(BASE_DIR, 'config.ini')
config.read(configFile)
class parseStock:
	def __init__(self, ticker, type):
		if type == 'price':
			url = config['StockInfoUrl']['Quote'].format(ticker, ticker)
		else:
			url = config['StockInfoUrl']['Profile'].format(ticker, ticker)
		for i in range(3):
			try:
				response = requests.get(url, verify=False, headers=self._get_headers(), timeout=30)
				self.parsedStock = html.fromstring(response.text)
			except requests.exceptions.RequestException as e:
				continue 
			else:
				break
		else:
			raise Exception("Unable to connect to a new server. Please check your internet connection.\n")	

	def _get_headers(self):
		return {"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-GB,en;q=0.9,en-US;q=0.8,ml;q=0.7",
            "cache-control": "max-age=0",
            "dnt": "1",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"}

	def get_price(self):
		try:
			return self.parsedStock.xpath('//span[@class="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"]')[0].text
		except:
			return '0.00'

	def get_sector(self):
		try:
			return self.parsedStock.xpath('//span[contains(text(), "Sector(s)")]/following-sibling::span')[0].text
		except:
			return 'N/A'

	def get_industry(self):
		try:
			return self.parsedStock.xpath('//span[contains(text(), "Industry")]/following-sibling::span')[0].text		
		except:
			return 'N/A'

	def get_earning_date(self):
		try:
			return self.parsedStock.xpath('//td[span[contains(text(), "Earnings Date")]]/following-sibling::td/span')[0].text
		except:
			pass



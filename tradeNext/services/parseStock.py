import requests
from lxml import html
class parseStock:
	def __init__(self, ticker, type):
		if type == 'price':
			url = "http://finance.yahoo.com/quote/%s?p=%s" % (ticker, ticker)
		else:
			url = "https://finance.yahoo.com/quote/%s/profile?p=%s" % (ticker, ticker)
		response = requests.get(url, verify=False, headers=self._get_headers(), timeout=30)
		try:
			self.parsedStock = html.fromstring(response.text)
		except:
			pass

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
		return self.parsedStock.xpath('//span[@class="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"]')[0].text

	def get_sector(self):
		return self.parsedStock.xpath('//span[contains(text(), "Sector(s)")]/following-sibling::span')[0].text

	def get_industry(self):
		return self.parsedStock.xpath('//span[contains(text(), "Industry")]/following-sibling::span')[0].text		

	def get_earning_date(self):
		return self.parsedStock.xpath('//td[span[contains(text(), "Earnings Date")]]/following-sibling::td/span')[0].text



from tradeNext.models import AssetDetails
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
def update_stock():
    assets = AssetDetails.objects.all()
    for asset in assets:
        try:
            asset.save()
            print("saving...\n" + asset.AssetId)
        except:
            pass

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_stock, 'interval', minutes=10)
    scheduler.start()

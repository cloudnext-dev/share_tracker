from tradeNext.models import AssetDetails
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import concurrent.futures
import configparser

def update_stock():
    assets = AssetDetails.objects.all()
    with concurrent.futures.ThreadPoolExecutor(max_workers=60) as executor:
            executor.map(lambda asset: asset.save(), assets)
    #for asset in assets:
    #    try:
    #        asset.save()
    #        print("saving...\n" + asset.AssetId)
    #    except:
    #        pass

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_stock, 'interval', minutes=30)
    scheduler.start()

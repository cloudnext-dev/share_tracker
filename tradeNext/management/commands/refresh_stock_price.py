from django.core.management.base import BaseCommand, CommandError
from tradeNext.models import AssetDetails
from yahoo_fin import stock_info as si

class Command(BaseCommand):
    help = 'Refesh Stock Pricee In Every 30(Mins)'

    def handle(self, *args, **options):
        try:
            assets = AssetDetails.objects.all()
            for asset in assets:
                try:
                    asset.save()
                    self.stdout.write(self.style.SUCCESS(asset.AssetId))
                    self.stdout.write(self.style.SUCCESS(asset.CurrentMarketPrice))
                except:
                    pass
        except:
            self.stdout.write(self.style.ERROR('Field "AssetId" does not exist.'))
            return

        self.stdout.write(self.style.SUCCESS('Successfully Updated all Asset Price'))
        return
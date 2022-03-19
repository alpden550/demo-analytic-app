from django.core.management import BaseCommand

from analytics.services.load_sample import load_sample_csv_dataset


class Command(BaseCommand):
    help = "Load sample isight data from csv"

    def handle(self, *args, **options):
        load_sample_csv_dataset()

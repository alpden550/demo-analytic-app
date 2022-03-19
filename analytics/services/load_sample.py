import csv

from analytics.models import Insight


def load_sample_csv_dataset(path: str = "analytics/samples/dataset.csv") -> None:
    insights = []

    with open(path) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            insights.append(Insight(**row))

    Insight.objects.bulk_create(insights)

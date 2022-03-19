import json

import maya
import pytest
from mixer.backend.django import mixer

from analytics.interfaces import InsightQueryBuilder


@pytest.mark.django_db
class TestInsightQueryBuilderFilters:
    @pytest.fixture(scope="class")
    def interface(self):
        return InsightQueryBuilder

    def test_query_with_broken_filters_return_queryset(self, interface):
        mixer.cycle(5).blend("analytics.Insight")

        query = interface({"filters": "{'date_from': 2017-06-10}"})
        assert query.build().count() == 5

    def test_query_with_date_from_filter(self, interface):
        old_date = maya.now().add(days=-10).date
        mixer.cycle(5).blend("analytics.Insight")
        mixer.cycle(5).blend("analytics.Insight", date=old_date)

        date_from = json.dumps({"date_from": f"{old_date.isoformat()}"})
        query = interface({"filters": f"{date_from}"})

        assert query.build().count() == 5

    def test_query_with_date_to_filter(self, interface):
        old_date_10 = maya.now().add(days=-10).date
        old_date_5 = maya.now().add(days=-5).date
        mixer.cycle(5).blend("analytics.Insight", date=old_date_5)
        mixer.cycle(5).blend("analytics.Insight", date=old_date_10)

        date_to = json.dumps({"date_to": f"{old_date_10.isoformat()}"})
        query = interface({"filters": f"{date_to}"})

        assert query.build().count() == 5

    def test_query_with_channel_filter(self, interface):
        mixer.cycle(5).blend("analytics.Insight", channel="vungle")
        mixer.cycle(5).blend("analytics.Insight", channel="adcolony")
        mixer.cycle(5).blend("analytics.Insight", channel="apple_search_ads")

        channel = json.dumps({"channel": "vungle"})
        query = interface({"filters": f"{channel}"})

        assert query.build().count() == 5

    def test_query_with_country_filter(self, interface):
        mixer.cycle(5).blend("analytics.Insight", country="UA")
        mixer.cycle(5).blend("analytics.Insight", country="CA")
        mixer.cycle(5).blend("analytics.Insight", country="GB")

        country = json.dumps({"country": "UA"})
        query = interface({"filters": f"{country}"})

        assert query.build().count() == 5

    def test_query_with_os_filter(self, interface):
        mixer.cycle(5).blend("analytics.Insight", os="ios")
        mixer.cycle(5).blend("analytics.Insight", os="android")

        os = json.dumps({"os": "ios"})
        query = interface({"filters": f"{os}"})

        assert query.build().count() == 5

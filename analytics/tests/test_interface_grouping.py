import maya
import pytest

from analytics.interfaces import InsightQueryBuilder
from mixer.backend.django import mixer
from django.core.exceptions import FieldError


@pytest.mark.django_db
class TestInsightQueryBuilderFilters:
    @pytest.fixture(scope="class")
    def interface(self):
        return InsightQueryBuilder

    def test_query_with_wrong_group_name(self, interface):
        query = interface({"grouping": "chanel"})
        with pytest.raises(FieldError):
            query.build()

    def test_query_group_by_day(self, interface):
        mixer.cycle(5).blend("analytics.Insight", date=maya.now().add(days=-1).date)
        mixer.cycle(5).blend("analytics.Insight", date=maya.now().add(days=-2).date)
        mixer.cycle(5).blend("analytics.Insight", date=maya.now().add(days=-3).date)

        query = interface({"grouping": "date"})

        assert query.build().count() == 3

    def test_query_group_by_month(self, interface):
        mixer.cycle(5).blend("analytics.Insight", date=maya.when("last month").snap("@month").date)
        mixer.cycle(5).blend("analytics.Insight", date=maya.now().date)
        mixer.cycle(5).blend("analytics.Insight", date=maya.now().snap("@month").date)

        query = interface({"grouping": "date__month"})

        assert query.build().count() == 2

    def test_query_group_by_year(self, interface):
        mixer.cycle(5).blend("analytics.Insight", date=maya.when("last year").snap("@month").date)
        mixer.cycle(5).blend("analytics.Insight", date=maya.now().date)
        mixer.cycle(5).blend("analytics.Insight", date=maya.now().snap("@month").date)

        query = interface({"grouping": "date__year"})

        assert query.build().count() == 2

    def test_query_group_by_os(self, interface):
        mixer.cycle(5).blend("analytics.Insight", os="ios")
        mixer.cycle(5).blend("analytics.Insight", os="android")

        query = interface({"grouping": "os"})

        assert query.build().count() == 2

    def test_query_group_by_country(self, interface):
        counties = ("RU", "US", "GB", "CA")
        for country in counties:
            mixer.cycle(5).blend("analytics.Insight", country=country)

        query = interface({"grouping": "country"})

        assert query.build().count() == 4

    def test_query_group_by_channel(self, interface):
        channels = ("adcolony", "apple_search_ads", "chartboost", "facebook", "google", "unityads", "vungle")
        for channel in channels:
            mixer.cycle(5).blend("analytics.Insight", channel=channel)

        query = interface({"grouping": "channel"})

        assert query.build().count() == 7

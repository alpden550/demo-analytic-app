import maya
import pytest
from django.core.exceptions import FieldError
from mixer.backend.django import mixer

from analytics.interfaces import InsightQueryBuilder


@pytest.mark.django_db
class TestInsightQueryBuilderOrdering:
    @pytest.fixture(scope="class")
    def interface(self):
        return InsightQueryBuilder

    def test_query_with_wrong_order_name(self, interface):
        query = interface({"ordering": "chanel"})
        with pytest.raises(FieldError):
            query.build()

    def test_query_order_by_date_desc(self, interface):
        mixer.cycle(5).blend("analytics.Insight", date=maya.now().add(days=-1).date)
        mixer.cycle(5).blend("analytics.Insight", date=maya.now().add(days=-2).date)
        mixer.cycle(5).blend("analytics.Insight", date=maya.now().add(days=-3).date)

        query = interface({"ordering": "-date"})

        assert query.build()[0].date == maya.now().add(days=-1).date

    def test_query_order_by_date_asc(self, interface):
        mixer.cycle(5).blend("analytics.Insight", date=maya.now().add(days=-1).date)
        mixer.cycle(5).blend("analytics.Insight", date=maya.now().add(days=-2).date)
        mixer.cycle(5).blend("analytics.Insight", date=maya.now().add(days=-3).date)

        query = interface({"ordering": "date"})

        assert query.build()[0].date == maya.now().add(days=-3).date

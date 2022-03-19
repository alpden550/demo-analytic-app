import pytest
from mixer.backend.django import mixer

from analytics.interfaces import InsightQueryBuilder


@pytest.mark.django_db
class TestInsightQueryBuilderCustomFields:
    @pytest.fixture(scope="class")
    def interface(self):
        return InsightQueryBuilder

    def test_query_calculate_cpi(self, interface):
        mixer.blend("analytics.Insight", spend=75.00, installs=35)
        mixer.blend("analytics.Insight", spend=128.00, installs=64)

        query = interface({"cpi": "true", "ordering": "cpi"}).build()

        assert round(query[0].cpi, 2) == 2.00
        assert round(query[1].cpi, 2) == 2.14

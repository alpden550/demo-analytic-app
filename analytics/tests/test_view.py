import pytest
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework import status


@pytest.mark.django_db
class TestInsightAPIView:
    URL = reverse("analytics:insights")

    def test_insights_list_view_url_exists(self, api_client):
        response = api_client.get(self.URL)
        assert response.status_code == status.HTTP_200_OK

    def test_insights_list_view(self, api_client):
        mixer.cycle(10).blend("analytics.Insight")
        response = api_client.get(self.URL)

        assert response.data["count"] == 10
        assert len(response.data["results"]) == 10

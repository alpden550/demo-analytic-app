from django.urls import path

from analytics.views import InsightListAPIView


app_name = "analytics"

urlpatterns = [
    path("insights/", InsightListAPIView.as_view(), name="insights"),
]

from django.contrib import admin
from rangefilter.filters import DateRangeFilter

from analytics.models import Insight


@admin.register(Insight)
class InsightAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "date",
        "channel",
        "country",
        "os",
        "impressions",
        "clicks",
        "installs",
        "spend",
        "revenue",
    )
    list_filter = (("date", DateRangeFilter), "channel", "country", "os")

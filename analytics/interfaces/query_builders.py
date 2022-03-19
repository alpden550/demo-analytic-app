import json
from typing import Union

import maya
from django.db.models import QuerySet, Q, F, Sum, ExpressionWrapper, FloatField
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth, TruncQuarter, TruncYear

from analytics.models import Insight


class InsightQueryBuilder:
    def __init__(self, params: dict[str, str]):
        self.filters: str | None = params.get("filters")
        self.grouping: str | None = params.get("grouping")
        self.ordering: str | None = params.get("ordering")
        self.cpi: str | None = params.get("cpi")

    def filter_queryset(self) -> Q:
        if self.filters is None:
            return Q()

        raw_filters = self.filters.replace("'", '"')
        query = Q()

        try:
            filters = json.loads(raw_filters)
        except json.JSONDecodeError:
            return query

        if "date_from" in filters:
            query &= Q(date__gte=maya.parse(filters["date_from"]).date)
        if "date_to" in filters:
            query &= Q(date__lte=maya.parse(filters["date_to"]).date)
        if "channel" in filters:
            query &= Q(channel=filters["channel"])
        if "country" in filters:
            query &= Q(country=filters["country"])
        if "os" in filters:
            query &= Q(os=filters["os"])

        return query

    @staticmethod
    def trunc_date(value: str) -> dict[str, Union[TruncDay, TruncWeek, TruncMonth, TruncQuarter, TruncYear]]:
        try:
            _, period = value.split("__")
        except ValueError:
            _, period = value, "day"

        match period:
            case "day":
                return {"insight_date": TruncDay("date")}
            case "week":
                return {"insight_date": TruncWeek("date")}
            case "month":
                return {"insight_date": TruncMonth("date")}
            case "quarter":
                return {"insight_date": TruncQuarter("date")}
            case "year":
                return {"insight_date": TruncYear("date")}

    def group_queryset(self, queryset: "QuerySet[Insight]") -> "QuerySet[Insight]":
        raw_grouping = self.grouping
        if raw_grouping is None:
            return queryset

        groups = raw_grouping.split(",")
        date = next((group for group in groups if group.startswith("date")), None)
        if date is not None:
            queryset = queryset.values(**self.trunc_date(date)).values(date=F("insight_date"))
            groups.remove(date)
            queryset = queryset.values(*groups, "date")
        else:
            queryset = queryset.values(*groups)

        return queryset.annotate(
            impressions=Sum("impressions"),
            clicks=Sum("clicks"),
            installs=Sum("installs"),
            spend=Sum("spend"),
            revenue=Sum("revenue"),
        )

    def sort_queryset(self, queryset: "QuerySet[Insight]") -> "QuerySet[Insight]":
        raw_ordering = self.ordering
        if raw_ordering is None:
            return queryset

        return queryset.order_by(*raw_ordering.split(","))

    def handle_cpi(self, queryset: "QuerySet[Insight]") -> "QuerySet[Insight]":
        cpi = self.cpi.lower() in {"1", "true"} if self.cpi else None
        if not cpi:
            return queryset

        return queryset.annotate(cpi=ExpressionWrapper(F("spend") / F("installs"), output_field=FloatField()))

    def build(self) -> "QuerySet[Insight]":
        queryset = Insight.objects.filter(self.filter_queryset())
        queryset = self.group_queryset(queryset)
        queryset = self.handle_cpi(queryset)
        queryset = self.sort_queryset(queryset)

        return queryset

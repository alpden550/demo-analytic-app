from django.core.exceptions import FieldError
from rest_framework import generics, status
from rest_framework.response import Response

from analytics.exceptions import QueryException
from analytics.interfaces import InsightQueryBuilder
from analytics.models import Insight
from analytics.serializers import InsightSerializer


class InsightListAPIView(generics.ListAPIView):
    serializer_class = InsightSerializer

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except QueryException as error:
            return Response({"detail": error.message}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        query_params = self.request.query_params
        if query_params:
            query_builder = InsightQueryBuilder(query_params)
            try:
                return query_builder.build()
            except (TypeError, FieldError):
                raise QueryException("Can't process values for grouping")

        return Insight.objects.all()

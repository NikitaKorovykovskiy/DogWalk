from django_filters import rest_framework as filters

from dw.models import WalkOrder

class OrderFilter(filters.FilterSet):
    date = filters.CharFilter(method="filter_by_date")


    class Meta:
        model = WalkOrder
        fields = ("start_time",)
    def filter_by_date(self, queryset, name, value):
        return queryset.filter(start_time__date=value)


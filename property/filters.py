from django.db.models import Q, F
from django_filters import FilterSet
# from django_filters.filters import CharFilter, NumberFilter, BooleanFilter
from property.models import Deal






# class DealFilter(FilterSet):
    # """
    # Report - Admin User > Courses > Category > Search Function > Search functionality isn’t working properly . All the courses get displayed with some random keyword.
    # Bug - BLI-478
    # Solution - Search by course title
    # """
    # category            = CharFilter(field_name="category__title", lookup_expr='icontains')
    # tags                = CharFilter(method="filter_by_tags")
    # query               = CharFilter(method='filter_multi_query')

    # def filter_by_tags(self, queryset, name, value):
    #     return queryset.filter(tags__title__icontains=value)

    # def filter_multi_query(self, queryset, name, value):
    #     return d.objects.filter(title__icontains=value,is_deleted=False)

    # class Meta:
        # model = Deal
        # fields = ['category', 'tags']
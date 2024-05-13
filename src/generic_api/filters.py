import django_filters
from rest_framework.filters import BaseFilterBackend

from .models import Post

class PostFilter(django_filters.FilterSet):

    title_icn = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    title_sw = django_filters.CharFilter(field_name='title', lookup_expr='startswith')
    content = django_filters.CharFilter(field_name='content', method='filter_contains_content')
    content_comment = django_filters.CharFilter(field_name='content', method='filter_comment')

    class Meta:
        model = Post
        fields = ('title',)

    def filter_contains_content(self, queryset, name, val):
        """
        Post の内容から検索
        """
        return queryset.filter(content__contains=val)
    
    def filter_comment(self, queryset, name, val):
        """
        Post に紐づく Comment の内容から検索
        """
        return queryset.filter(comments__comment__contains=val)


class CustomFilterBackend(BaseFilterBackend):

    def filter_queryset(self, req, queryset, view):
        params = req.query_params
        filter_queryset = queryset

        if 'title' in params.keys():
            filter_queryset = filter_queryset.filter(title=params['title'])
        
        if 'title_sw' in params.keys():
            filter_queryset = filter_queryset.filter(title__startswith=params['title_sw'])
        
        if 'title_ew' in params.keys():
            filter_queryset = filter_queryset.filter(title__endswith=params['title_ew'])
        
        if 'order_by' in params.keys():
            filter_queryset = filter_queryset.order_by(params['order_by'])
        
        return filter_queryset

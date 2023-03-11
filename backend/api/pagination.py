from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination


class LimitPageNumberPaginator(PageNumberPagination):
    '''Pagination with others parameters.'''
    django_paginator_class = Paginator
    page_query_param = 'page'
    page_size_query_param = 'limit'

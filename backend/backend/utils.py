from rest_framework.pagination import PageNumberPagination

class TaskPagination(PageNumberPagination):
    page_size = 2  # default items per page
    page_size_query_param = 'page_size'  # client can override per request
    max_page_size = 50

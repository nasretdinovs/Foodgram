from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    """Пагинатор с выводом определенного кол-ва страниц (limit)."""
    page_size_query_param = 'limit'

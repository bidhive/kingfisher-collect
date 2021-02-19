from collections import OrderedDict
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter

# NOTE(alec): Copied from bidhive-api
class DefaultPagination(PageNumberPagination):
    page_size = 25
    page_query_param = "page"
    page_size_query_param = "limit"
    max_page_size = 200

    def paginate_queryset(self, queryset, request, view=None):
        """
        Does default pagination, but performs ordering on the entire queryset. For some reason, sometimes
        having an order query parameter gets ignored - if you have 10 pages of customers and sort page 2 based on their name
        then the result is always the same. By forcefully ordering the queryset, this ensures that the result will be ordered.
        """
        ordering = request.query_params.get("ordering")
        if ordering:
            queryset = queryset.order_by(ordering)
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        next_page = None
        prev_page = None
        if self.page.has_next():
            next_page = self.page.next_page_number()
        if self.page.has_previous():
            prev_page = self.page.previous_page_number()

        return Response(
            OrderedDict(
                [
                    ("count", self.page.paginator.count),
                    ("limit", self.get_page_size(self.request)),
                    (
                        "page",
                        int(self.request.query_params.get(self.page_query_param, 1)),
                    ),
                    ("page_count", self.page.paginator.num_pages),
                    ("next", next_page),
                    ("previous", prev_page),
                    ("results", data),
                ]
            )
        )


class SubstringSearchFilter(SearchFilter):
    def get_search_terms(self, request):
        # NOTE(johan): The default SearchFilter actually splits search terms on spaces. For
        # now we just override this to only generate a single search term
        return [request.query_params.get(self.search_param, "")]
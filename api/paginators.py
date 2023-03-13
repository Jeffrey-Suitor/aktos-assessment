from dataclasses import dataclass
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.utils.urls import remove_query_param, replace_query_param


@dataclass
class LinkPaginator():
    
    def __init__(self, page_size: int, items_list: list) -> None:
        self.page_size = page_size
        self.items_list = items_list
        self.paginator = Paginator(items_list, page_size)
        
    def get_page_results(self, page: int):
        if not page or page < 1:
            raise Exception("Page number must be provided and atleast 1")
        try:
            return self.paginator.page(page)
        except PageNotAnInteger:
            return self.paginator.page(1)
        except EmptyPage:
            return self.paginator.page(self.paginator.num_pages)
        
    def set_page_size(self, page_size: int):
        if not page_size or page_size < 1:
            raise Exception("Page number must be provided and atleast 1")
        self.page_size = page_size
        self.paginator = Paginator(self.items_list, page_size)
        
    def set_items_list(self, items_list: list):
        self.items_list = items_list
        self.paginator = Paginator(items_list, self.page_size)
        
    def get_last_page(self):
        return self.paginator.num_pages
        
    def get_headers(self, page: int, url: str):
        if not page or page < 1:
            raise Exception("Page number must be provided and atleast 1")
        
        page = min(page, self.paginator.num_pages)
        relations = {
            'first': replace_query_param(url, 'page', 1),
            'last': replace_query_param(url, 'page', self.get_last_page()),
            'next': replace_query_param(url, 'page', page + 1) if page < self.get_last_page() else None,
            'prev': replace_query_param(url, 'page', page - 1) if page > 1 else None,
        }
        
        headers = ['<{}>; rel="{}"'.format(value, key) for key, value in relations.items() if value]
        return {"Link": ", ".join(headers)}
                        
from django.test import TestCase, Client
from ..models import Consumer
from ..paginators import LinkPaginator
from api.serializers import ConsumerSerializer

client = Client()

class PaginationTest(TestCase):
    def setUp(self):
        for i in range(0, 60):
            Consumer.objects.create(
                id=i,
                street="579 Mission Trl",
                status="collected",
                previous_jobs_count=1,
                amount_due=1000,
                lat=33.38935574,
                lng=-112.0882128,    
            )
            
    def test_pagination_get_consumers_first_page(self):
        paginator = LinkPaginator(10, Consumer.objects.all())
        paginator_results = ConsumerSerializer(paginator.get_page_results(1), many=True).data
        expected_results = ConsumerSerializer(Consumer.objects.filter(id__in=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]), many=True).data
        self.assertEqual(paginator_results, expected_results)
        self.assertEqual(paginator.get_last_page(), 6)
        
    def test_pagination_get_consumers_offset_page(self):
        paginator = LinkPaginator(10, Consumer.objects.all())
        paginator_results = ConsumerSerializer(paginator.get_page_results(2), many=True).data
        expected_results = ConsumerSerializer(Consumer.objects.filter(id__in=[10, 11, 12, 13, 14, 15, 16, 17, 18, 19]), many=True).data
        self.assertEqual(paginator_results, expected_results)

    def test_pagination_headers(self):
        paginator = LinkPaginator(10, Consumer.objects.all())
        headers = paginator.get_headers(2, 'http://127.0.0.1:8000/consumers?page=2')
        expected_links = [
            '<http://127.0.0.1:8000/consumers?page=1>; rel="first"', 
            '<http://127.0.0.1:8000/consumers?page=6>; rel="last"', 
            '<http://127.0.0.1:8000/consumers?page=3>; rel="next"', 
            '<http://127.0.0.1:8000/consumers?page=1>; rel="prev"'
        ]
        self.assertEqual(headers['Link'], ", ".join(expected_links))

        

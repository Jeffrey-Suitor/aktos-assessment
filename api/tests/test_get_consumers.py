from django.test import TestCase, Client
from api.serializers import ConsumerSerializer
from ..models import Consumer
from rest_framework import status
from django.urls import reverse
from ..helpers import consumer_dict_array_to_geojson_output

# Initialize the APIClient
client = Client()

class ConsumerTest(TestCase):
    """Test module for GET Consumer API"""

    def setUp(self):
        Consumer.objects.create(
            id=0,
            street="579 Mission Trl",
            status="collected",
            previous_jobs_count=1,
            amount_due=1000,
            lat=33.38935574,
            lng=-112.0882128,
        )
        Consumer.objects.create(
            id=1,
            street="578 Blake Ave",
            status="in_progress",
            previous_jobs_count=2,
            amount_due=1000,
            lat=33.41247393,
            lng=-112.2808164,
        )
        Consumer.objects.create(
            id=2,
            street="177 Blake Dv",
            status="collected",
            previous_jobs_count=1,
            amount_due=1001,
            lat=33.45330367,
            lng=-112.2324875,
        )
        Consumer.objects.create(
            id = 10,
            street = "293 9th St",
            status = "in_progress",
            previous_jobs_count = 3,
            amount_due = 1002,
            lat = 33.56081451,
            lng = -111.9265168,
        )
            

    def test_get_all_consumers(self):
        response = client.get(reverse('get_consumers'))
        consumers = Consumer.objects.all()
        serializer = ConsumerSerializer(consumers, many=True)
        output = consumer_dict_array_to_geojson_output(serializer.data)
        self.assertEqual(response.data, output)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_consumers_with_collected_status(self):
        response = client.get(reverse('get_consumers'), {'status': 'collected'}, format="json")
        consumers = Consumer.objects.all().filter(status='collected')
        serializer = ConsumerSerializer(consumers, many=True)
        output = consumer_dict_array_to_geojson_output(serializer.data)
        self.assertEqual(response.data, output)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_invalid_get_consumer_status(self):
        response = client.get(reverse('get_consumers'), {'status': 'invalid'}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_get_exact_previous_job_count(self):
        response = client.get(reverse('get_consumers'), {'previous_jobs_count': 3}, format="json")
        consumers = Consumer.objects.all().filter(previous_jobs_count=3)
        serializer = ConsumerSerializer(consumers, many=True)
        output = consumer_dict_array_to_geojson_output(serializer.data)
        self.assertEqual(response.data, output)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_consumers_with_min_previous_jobs_count(self):
        response = client.get(reverse('get_consumers'), {'min_previous_jobs_count': 2}, format="json")
        consumers = Consumer.objects.all().filter(previous_jobs_count__gte=2)
        serializer = ConsumerSerializer(consumers, many=True)        
        output = consumer_dict_array_to_geojson_output(serializer.data)
        self.assertEqual(response.data, output)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_consumers_with_max_previous_jobs_count(self):
        response = client.get(reverse('get_consumers'), {'max_previous_jobs_count': 1}, format="json")
        consumers = Consumer.objects.all().filter(previous_jobs_count__lt=2)
        serializer = ConsumerSerializer(consumers, many=True)
        output = consumer_dict_array_to_geojson_output(serializer.data)
        self.assertEqual(response.data, output)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_consumers_with_min_and_max_previous_jobs_count(self):
        response = client.get(reverse('get_consumers'), {'min_previous_jobs_count': 1, 'max_previous_jobs_count': 2}, format="json")
        consumers = Consumer.objects.all().filter(previous_jobs_count__gte=1, previous_jobs_count__lte=2)
        serializer = ConsumerSerializer(consumers, many=True)
        output = consumer_dict_array_to_geojson_output(serializer.data)
        self.assertEqual(response.data, output)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_consumers_with_min_and_max_previous_jobs_count_and_status(self):
        response = client.get(reverse('get_consumers'), {'min_previous_jobs_count': 1, 'max_previous_jobs_count': 2, 'status': 'collected'}, format="json")
        consumers = Consumer.objects.all().filter(previous_jobs_count__gte=1, previous_jobs_count__lte=2, status='collected')
        serializer = ConsumerSerializer(consumers, many=True)
        output = consumer_dict_array_to_geojson_output(serializer.data)
        self.assertEqual(response.data, output)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_invalid_query_with_min_and_max_and_exact_previous_jobs_count(self):
        response = client.get(reverse('get_consumers'), {'min_previous_jobs_count': 2, 'max_previous_jobs_count': 1, 'previous_jobs_count': 0}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_invalid_query_min_below_0(self):
        response = client.get(reverse('get_consumers'), {'min_previous_jobs_count': -1}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_invalid_query_min_above_max(self):
        response = client.get(reverse('get_consumers'), {'min_previous_jobs_count': 2, 'max_previous_jobs_count': 1}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)         
        
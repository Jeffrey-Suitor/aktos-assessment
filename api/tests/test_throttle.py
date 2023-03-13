from django.test import TestCase, Client
from ..models import Consumer
from rest_framework import status
from django.urls import reverse

client = Client()

class ThrottleTest(TestCase):
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

    def test_throttling_get_consumers(self):
        for i in range(0, 60):
            client.get(reverse("get_consumers"))
        response = client.get(reverse("get_consumers"))
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

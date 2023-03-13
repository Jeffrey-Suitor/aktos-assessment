from django.test import TestCase
from api.serializers import ConsumerSerializer
from ..models import Consumer
from ..helpers import consumer_dict_array_to_geojson_output


class GeojsonTest(TestCase):
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

    def test_geojson_output(self):
        consumers = Consumer.objects.all()
        serializer = ConsumerSerializer(consumers, many=True)
        output = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [-112.0882128, 33.38935574],
                    },
                    "properties": {
                        "id": 0,
                        "street": "579 Mission Trl",
                        "status": "collected",
                        "previous_jobs_count": 1,
                        "amount_due": 1000,
                    },
                }
            ],
        }
        self.assertEqual(consumer_dict_array_to_geojson_output(serializer.data), output)

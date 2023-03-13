def convert_consumer_dict_to_geojson_feature(consumer):
    return {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [consumer['lng'], consumer['lat']]},
            "properties": {
                'id': consumer['id'],
                'street': consumer['street'],
                'status': consumer['status'],
                'previous_jobs_count': consumer['previous_jobs_count'],
                'amount_due': consumer['amount_due']
            }
        }
    
def consumer_dict_array_to_geojson_output(consumer_dict_array):
    return {
        "type": "FeatureCollection",
        "features": list(map(lambda x: convert_consumer_dict_to_geojson_feature(x), consumer_dict_array))
    }
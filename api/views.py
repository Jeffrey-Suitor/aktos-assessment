from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, throttle_classes
from .models import Consumer
from .serializers import ConsumerSerializer
from .throttles import BurstThrottle, ContinousThrottle
from rest_framework import status as http_status
from .helpers import consumer_dict_array_to_geojson_output
from .paginators import LinkPaginator
from rest_framework.utils.urls import remove_query_param, replace_query_param

# Create your views here.
@api_view(["GET"])
@throttle_classes([BurstThrottle, ContinousThrottle])
def get_consumers(request):    
    # Get query params
    min_previous_jobs_count = request.query_params.get("min_previous_jobs_count", None)
    max_previous_jobs_count = request.query_params.get("max_previous_jobs_count", None)
    previous_jobs_count = request.query_params.get("previous_jobs_count", None)
    status = request.query_params.get("status", None)
    page = request.query_params.get("page", 1)
    page_size = request.query_params.get("page_size", 10)

    # Conver to integers if they exist
    min_previous_jobs_count = int(min_previous_jobs_count) if min_previous_jobs_count else None
    max_previous_jobs_count = int(max_previous_jobs_count) if max_previous_jobs_count else None
    previous_jobs_count = int(previous_jobs_count) if previous_jobs_count else None
    page = int(page) if page else None
    page_size = int(page_size) if page_size else None
    
    # Set default page values for pagination
    page = 1 if page < 1 else page
    page_size = 1 if page_size < 1 else page_size
    
    # Error checking
    if min_previous_jobs_count and max_previous_jobs_count and min_previous_jobs_count > max_previous_jobs_count:
        return Response(status=http_status.HTTP_400_BAD_REQUEST, data={"error": "Your query is invalid. The minimum previous jobs count must be less than the maximum previous jobs count."})
    
    if min_previous_jobs_count and min_previous_jobs_count < 0:
        return Response(status=http_status.HTTP_400_BAD_REQUEST, data={"error": "Your query is invalid. The minimum previous jobs count must be greater than 0."})
    
    if status and status not in Consumer.STATUS:
        return Response(status=http_status.HTTP_400_BAD_REQUEST, data={"error": "Your query is invalid. The status you provided is not valid."})

    # I decided to throw an error here because it's not clear what the expected behaviour
    # I could have been permissive and just take the previous_job_count as the priority but I would rather force the user to be explicit
    if previous_jobs_count is not None and (min_previous_jobs_count is not None or max_previous_jobs_count is not None):
        return Response(status=http_status.HTTP_400_BAD_REQUEST, data={"error": "Your query is invalid. Either provide a range for previous jobs or an exact count not both."})

    # Get consumers
    consumers = Consumer.objects.all()

    if min_previous_jobs_count:
        consumers = consumers.filter(previous_jobs_count__gte=min_previous_jobs_count)
    if max_previous_jobs_count:
        consumers = consumers.filter(previous_jobs_count__lte=max_previous_jobs_count)
    if previous_jobs_count:
        consumers = consumers.filter(previous_jobs_count=previous_jobs_count)
    if status:
        consumers = consumers.filter(status=status)
  
    # paginate and get link headers      
    paginator = LinkPaginator(page_size, consumers)
    consumers = paginator.get_page_results(page)
    headers = paginator.get_headers(page, request.build_absolute_uri())   
                 
    serializer = ConsumerSerializer(consumers, many=True)
    return Response(consumer_dict_array_to_geojson_output(serializer.data), headers=headers)
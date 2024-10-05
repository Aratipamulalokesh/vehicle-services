from rest_framework.response import Response
from rest_framework.decorators import api_view
from . import serializer
from . import models
from. models import VehicleIssue
from django.db.models import Sum
# Create your views here.

def componentExists(data: dict) -> bool:
    return True if models.Component.objects.filter(
        name = data.get('name'), price = data.get('price')
    ) else False

@api_view(['post'])
def add_component(request):
    print(request.data)
    response_query = ('name', 'price', 'repair_price', 'is_new')
    for query in response_query:
        if query not in request.data:
            return Response({
                'Error': f'{query} not found!'
            }, status=404)
    serialized_data = serializer.ComponentSerializer(data = request.data)
    if serialized_data.is_valid(raise_exception=True) and not componentExists(request.data):
        serialized_data.save()
        return Response({'response': 'Query Successful'}, status=200)
    return Response({'Error': 'Invalid Request!'})

@api_view(['post'])
def get_service_cost(request):
    response_query = ('vehicle_name', 'model_no', 'part_name', 'is_repair')
    for query in response_query:
        if query not in request.data:
            return Response({
                'Error': f'{query} not found!'
            })
        
    part_name, is_repair = request.data.get('part_name'), request.data.get('is_repair')
    response = models.Component.objects.filter(name = part_name).first()
    return Response({
        'part_name': part_name, 
        'status': 'new',
        'price': response.price
    } if not is_repair else {
        'part_name': part_name, 
        'status': 'new',
        'price': response.repair_price
    }) if response else Response({
        'Error': 'Invalid Request!'
    })

@api_view(['post'])
def add_vehicle_for_service(request):
    response_query = ('name', 'model', 'part_name', 'is_repair', 'register')
    for query in response_query:
        if query not in request.data:
            return Response({
                'Error': f'{query} not found!'
            })

    serialized_vehicle_data = serializer.VehicleSerializer(data = request.data)
    if serialized_vehicle_data.is_valid(raise_exception=True):
        serialized_vehicle_data.save()

    request.data['component'] = models.Component.objects.get(
        name = request.data.get('part_name')
    ).pk
    request.data['vehicle'] = models.Vehicle.objects.get(
        name = request.data.get('name'), model = request.data.get('model')
    ).pk

    serialized_issue_data = serializer.VehicleIssueSerializer(data = request.data)
    if serialized_issue_data.is_valid(raise_exception = True):
        serialized_issue_data.save()
        return Response({
            'status': 'Success',
            'Appointment': 'Booked!'
        })
    models.Vehicle.objects.delete(name = request.get('name'), model = request.data.get('model'))
    
    return Response({
        'Error': 'Invalid Response!'
    })


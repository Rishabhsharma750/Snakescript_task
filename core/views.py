from django.shortcuts import render
from rest_framework.decorators import action
from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny,IsAuthenticatedOrReadOnly,IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend

class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    filter_backends = (DjangoFilterBackend,SearchFilter,OrderingFilter)
    filterset_fields = ['name',]
    search_fields = ['name', 'address']
    ordering_fields = ['id', 'name','address']
    ordering =('id',)
    lookup_field = 'doc_num'
    authentication_classes = [TokenAuthentication,]

    def get_queryset(self):
        name = self.request.query_params.get('name',None)
        if self.request.query_params.get('active') == 'False':
            status = False
        else:
            status = True
        if name:
            customers=Customer.objects.filter(name__icontains=name,active=status)
        else:
            customers=Customer.objects.filter(active=status)
        return customers

    # def list(self, request, *args, **kwargs):
    #     customers = self.get_queryset()
    #     serializer= CustomerSerializer(customers,many=True)
    #     return Response(serializer.data)


    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = CustomerSerializer(obj)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data
        customer = Customer.objects.create(
            name = data['name'],address=data['address'],data_sheet_id=data['data_sheet']
        )
        profession=Profession.objects.get(id=data['profession'])
        customer.professions.add(profession)
        customer.save()
        serializer=CustomerSerializer(customer)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        customer=self.get_object()
        data=request.data
        customer.name=data['name']
        customer.address=data['address']
        customer.data_sheet_id=data['data_sheet']
        profession=Profession.objects.get(id=data['profession'])
        
        for p in customer.professions.all():
            customer.professions.remove(p)
        customer.professions.add(profession)
        customer.save()
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        customer=self.get_object()
        customer.name=request.data.get('name',customer.name)
        customer.address=request.data.get('address',customer.address)
        customer.data_sheet_id=request.data.get('data_sheet',customer.data_sheet_id)
        customer.save()
        serializer=CustomerSerializer(customer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        customer=self.get_object()
        customer.delete()
        return Response('Object removed')

    @action(detail=True)
    def deactivate(self,request,**kwargs):
        customer=self.get_object()
        customer.active=False
        customer.save()
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    @action(detail=False)
    def deactivate_all(self,request,**kwargs):
        customer=Customer.objects.all()
        customer.update(active=False)
        serializer=CustomerSerializer(customer,many=True)
        return Response(serializer.data)

    @action(detail=False)
    def activate_all(self,request,**kwargs):
        customer=self.get_queryset()
        customer.update(active=True)
        serializer=CustomerSerializer(customer,many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def change_status(self,request,**kwargs):
        if request.data['active']=='True':
            status=True
        else:
            status=False
        customer = self.get_queryset()
        print(status)
        customer.update(active=status)
        serializer = CustomerSerializer(customer, many=True)
        return Response(serializer.data)


class ProfessionViewSet(viewsets.ModelViewSet):
    serializer_class = ProfessionSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAdminUser, ]

    def get_queryset(self):
        queryset = Profession.objects.all()
        return queryset

class DataSheetViewSet(viewsets.ModelViewSet):
    serializer_class = DataSheetSerializer
    permission_classes = [AllowAny,]

    def get_queryset(self):
        queryset = DataSheet.objects.all()
        return queryset

class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticatedOrReadOnly,]

    def get_queryset(self):
        queryset = Document.objects.all()
        return queryset
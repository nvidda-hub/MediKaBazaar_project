from django.http import Http404
from django.shortcuts import render
from django.shortcuts import render, redirect 
from medi_webapp.serializers import ProductSerializer
from medi_webapp.models import Product
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser

# Create your views here.
import pymongo
from django.db.models.query_utils import Q
from rest_framework.views import APIView


db_client = pymongo.MongoClient('mongodb://localhost:27017/')
db = db_client.product_database



class ProductView(APIView):
    def get(self, request, format=None):
        product = Product.objects.all()
        serializer = ProductSerializer(product, many=True)
        return render(request, 'medi_webapp/products.html', {'products':serializer.data})
  
    # POST request for creating new alert/targetPrice
    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            product = Product.objects.all()
            serializer = ProductSerializer(product, many=True)
            return render(request, 'medi_webapp/products.html', {'products':serializer.data})
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return 

    def put(self, request, format=None):
        Product = Product.objects.get(id = request.data['id'])
        serializer = ProductSerializer(Product, data=request.data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PATCH request to edit partial data { In this you can flag to an item }
    def patch(self, request, format=None):
        Product = Product.objects.get(id = request.data['id'])
        serializer = ProductSerializer(Product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # this DELETE request will delete the data from database
    def delete(self, request, format=None):
        if self.request.user.is_authenticated:
            Product = Product.objects.get(id = request.data['id'])
            Product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
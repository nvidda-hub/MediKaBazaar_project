from django.http import Http404
from django.shortcuts import render
from django.shortcuts import render, redirect 
from medi_webapp.serializers import ProductSerializer
from medi_webapp.models import Product
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.pagination import LimitOffsetPagination
from medi_webapp.documents import ProductDocument

# Create your views here.
import pymongo
from elasticsearch_dsl import Q
from rest_framework.views import APIView


db_client = pymongo.MongoClient('mongodb://localhost:27017/')
db = db_client.product_database



class ProductView(APIView):
    def get(self, request, pk=None, format=None):
        if pk:
            try:
                product_obj = Product.objects.get(pk=pk)
            except:
                return Response({"msg":f"Record for id {pk} Not found!!"})

            serializer = ProductSerializer(product_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
            

    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            product = serializer.save()
            data['response'] = "successfully added new product."
            data['product_name'] = product.product_name
            data['quantity'] = product.quantity
            data['price'] = product.price
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    def get(self, request, pk=None):
        try:
            product_obj = Product.objects.get(pk=pk)
        except:
            return Response({"msg":f"Record for id {pk} Not found!!"})

        serializer = ProductSerializer(product_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

    def put(self, request, pk, format=None):            
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':f'id {pk} Data updated successfully!'}, status=status.HTTP_226_IM_USED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # partial update
    def patch(self, request, pk, format=None):
        try:
            product = Product.objects.get(pk=pk)
        except:
            return Response({"msg":f"data of student with id {pk} not found!!"})
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':f'id : {pk} patially Data updated successfully!'}, status=status.HTTP_226_IM_USED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            product = Product.objects.get(pk=pk)
        except:
            return Response({"msg":f"data of student with id {pk} not found!!"})

        product.delete()
        return Response({"msg":f"data of student with id {pk} deleted!!"})


class ProductSearchView(APIView, LimitOffsetPagination):
    product_search_serializer = ProductSerializer
    search_document = ProductDocument

    def get(self, request, query):
        try:
            # creating query instance
            q = Q(
                "multi_match",
                query=query,
                fields=[
                    "product_name"
                    ],
            )

            search = self.search_document.search().query(q)
            response = search.execute()

            results = self.paginate_queryset(response, request, view=self)
            serializer = self.product_search_serializer(results, many=True)

            return self.get_paginated_response(serializer.data)


        except:
            return Response({"msg":f"data not found for product name {query}!!"}, status=status.HTTP_404_NOT_FOUND)
from django.urls import path

from medi_webapp import views


app_name = 'medi_webapp'

urlpatterns = [
    path('', views.ProductView.as_view(), name='products')
]
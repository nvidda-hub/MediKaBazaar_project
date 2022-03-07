from django.urls import path

from medi_webapp import views


app_name = 'medi_webapp'

urlpatterns = [
    path('products/', views.ProductView.as_view(), name='products'),
    path('products/search/<str:query>/', views.ProductSearchView.as_view(), name='productsearch'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='products_detail')
]
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('products.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
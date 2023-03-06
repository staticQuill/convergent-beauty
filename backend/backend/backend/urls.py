from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/', include('products.urls')),
    path('api/', include('recommendations.urls')),
    path('api/search/', include('search.urls')),
    path('api/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/auth/', include('auth.urls'))
]
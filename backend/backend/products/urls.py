from django.urls import path

from . import views

urlpatterns = [
    path('user-products/', views.UserProductView.as_view(), name='create-user-product')
]
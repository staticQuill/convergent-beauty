from django.urls import path

from backend.products import views

urlpatterns = [
    path('user-products/', views.UserProductView.as_view(), name='create-user-product')
]
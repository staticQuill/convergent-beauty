from django.urls import path

from . import views

urlpatterns = [
    path('autocomplete/', views.SearchAutocompleteView.as_view(), name='autocomplete'),
]
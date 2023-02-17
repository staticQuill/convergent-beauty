from django.urls import path

from . import views

urlpatterns = [
    path('preferences/', views.UserPreferenceView.as_view(), name='preferences'),
    path('recommendations/', views.RecommendationView.as_view(), name='recommendations')
]
from django.urls import path

from . import views

urlpatterns = [
    path('preferences/', views.UserPreferenceView.as_view(), name='user-preferences')
]
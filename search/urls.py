from django.urls import path
from search import views

app_name = 'search'

urlpatterns = [
    path('', views.SearchPage.as_view(), name='me'),
    path('results/', views.SearchResult.as_view(), name='results'),
]

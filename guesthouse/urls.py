from django.urls import path

from . import views


urlpatterns = [
    path('', views.LocationsView.as_view()),
    path('filter/', views.FilterLocationView.as_view(), name='filter'),
    path('search/', views.Search.as_view(), name='search'),
    path('<slug:slug>/', views.LocationDetailView.as_view(), name='location_detail'),

    path('ru/export_to_csv', views.export_to_csv, name='export_to_csv')
]

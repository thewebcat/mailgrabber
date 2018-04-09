from django.urls import path

from search import views

urlpatterns = [
    path('', views.search_form, name='search_form'),
    path('filter/', views.search, name='search')
]
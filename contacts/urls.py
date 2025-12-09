from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search_contacts, name='search'),
    path('create/', views.create_contact, name='create-contact'),
    path('contacts/<int:contact_id>/delete/', views.contact_delete, name="contact_delete"),
]

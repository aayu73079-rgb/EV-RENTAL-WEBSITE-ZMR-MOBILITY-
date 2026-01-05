# from django.urls import path
# from ZMR_MOBILTY_APP import views
# from django.urls import path, include
# from . import views


# urlpatterns = [
#     path('',views.base,name="base"),
#     # path('about/', views.about, name='about'),
#     path('home/', views.home, name='home'),
#     path('contact/', views.contact, name='contact'),
#     path('market/', views.market, name='market'),
#     path('team/', views.team, name='team'),
#     path('services/', views.services, name='services'),
#     path('locations/', views.services, name='locations'),
#      path('', views.home, name='home'),
#     path('contact/', views.contact, name='contact'),
#     path('franchise/', views.franchise, name='franchise'),
#     path('services/', views.services, name='services'),
#     path('locations/', views.locations, name='locations'),
    
#     path('contact/', views.contact_view, name='contact'),

    
# ]


# test code
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    path('home/', views.home, name='home'),
    path('contact/', views.contact_view, name='contact'),
    path('contact/success/', views.contact_success, name='contact_success'),
    path('franchise/', views.franchise_application, name='franchise'),
    path('rental/', views.rental_booking, name='rental'),
    path('vehicles/', views.VehicleListView.as_view(), name='vehicles'),
    path('vehicle/<int:pk>/', views.VehicleDetailView.as_view(), name='vehicle_detail'),
    path('services/', views.services_view, name='services'),
    path('locations/', views.locations_view, name='locations'),
    path('api/vehicle-price/', views.get_vehicle_price, name='vehicle_price'),
]
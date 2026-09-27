# accounts/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('client-dashboard/', views.client_dashboard, name='client_dashboard'),
    path('artisan-dashboard/', views.artisan_dashboard, name='artisan_dashboard'),
    path('publish-service/', views.publish_service, name='publish_service'),
    path('edit-service/<int:pk>/', views.edit_service, name='edit_service'),
    path('delete-service/<int:pk>/', views.delete_service, name='delete_service'),
    path('client-services/', views.client_services, name='client_services'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('demand-service/<int:service_id>/', views.demand_service, name='demand_service'),
    path('accept-demand/<int:demand_id>/', views.accept_demand, name='accept_demand'),
    path('refuse-demand/<int:demand_id>/', views.refuse_demand, name='refuse_demand'),
    path('service-status/', views.service_status_list, name='service_status_list'),
    path('service-status/<int:service_id>/', views.service_status_detail, name='service_status_detail'),
    path('demand-services/', views.demand_services, name='demand_services'), 
    path('artisan/services/', views.artisan_services, name='artisan_services'),
    path('artisan/services/edit/<int:service_id>/', views.edit_service, name='edit_service'),
     path('Home/', views.home, name='index'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('service/', views.service, name='service'),
    ]

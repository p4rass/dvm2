from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('ticket-booking/', views.ticket_booking, name='ticket_booking'),
    path('book-ticket/<int:bus_id>/', views.book_ticket, name='book_ticket'),
    path('booking-success/<int:booking_id>/', views.booking_success, name='booking_success'),
    path('add-money/', views.add_money, name='add_money'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add-bus/', views.add_bus, name='add_bus'),
]
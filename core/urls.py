# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    # Add these two new lines
    path('log/<str:transaction_type>/', views.transaction_log_view, name='transaction_log'),
    path('partner/<int:partner_id>/log/', views.partner_log_view, name='partner_log'),
]
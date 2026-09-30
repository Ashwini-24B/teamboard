from django.urls import path
from . import views

urlpatterns = [
    path('auth/register/', views.RegistrationView.as_view(), name='register'),
    path('kb/query/', views.KBQueryView.as_view(), name='kb-query'),
    path('admin/usage-summary/', views.UsageSummaryView.as_view(), name='usage-summary'),
    path('knowledge/', views.KBEntryListCreateView.as_view(), name='knowledge-list'),
    path('knowledge/<int:pk>/', views.KBEntryDetailView.as_view(), name='knowledge-detail'),
]
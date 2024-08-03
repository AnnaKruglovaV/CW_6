from django.urls import path
from django.views.decorators.cache import cache_page

from mailings.apps import ServiceConfig
from mailings.views import ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, ClientDeleteView, \
    MailingSettingsListView, MailingSettingsDetailView, MailingSettingsCreateView, MailingSettingsUpdateView, \
    MailingSettingsDeleteView, LogListView, HomePageView

app_name = ServiceConfig.name

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('client_list/', ClientListView.as_view(), name='client_list'),
    path('mailings/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('mailings/create/', ClientCreateView.as_view(), name='client_create'),
    path('mailings/<int:pk>/update/', ClientUpdateView.as_view(), name='client_update'),
    path('mailings/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),
    path('mailings', MailingSettingsListView.as_view(), name='mailingsettings_list'),
    path('mailingsettings/<int:pk>/', cache_page(60)(MailingSettingsDetailView.as_view()),
         name='mailingsettings_detail'),
    path('mailingsettings/create/', MailingSettingsCreateView.as_view(), name='mailingsettings_create'),
    path('mailingsettings/<int:pk>/update/', MailingSettingsUpdateView.as_view(), name='mailingsettings_update'),
    path('mailingsettings/<int:pk>/delete/', MailingSettingsDeleteView.as_view(), name='mailingsettings_delete'),
    path('logs_list/', LogListView.as_view(), name='logs_list'),
]

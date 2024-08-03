from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from blog.services import get_articles_from_cache
from mailings.forms import MailingSettingsForm, ModeratorMailingSettingsForm
from mailings.models import Client, MailingSettings, Log


class HomePageView(TemplateView):
    template_name = 'mailings/home_page.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        mailings = MailingSettings.objects.all()
        clients = Client.objects.all()
        context_data['all_mailings'] = mailings.count()
        context_data['active_mailings'] = mailings.filter(status=MailingSettings.STARTED).count()
        context_data['active_clients'] = clients.values('email').distinct().count()

#        context_data['random_blogs'] = get_articles_from_cache().order_by('?')[:3]
        return context_data


class ClientListView(ListView):
    model = Client


class ClientDetailView(DetailView):
    model = Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    fields = ('name', 'email', 'comment')
    success_url = reverse_lazy('mailings:client_list')

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.owner = user
        client.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    fields = ('name', 'email', 'comment')
    success_url = reverse_lazy('mailings:client_list')


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailings:client_list')


class MailingSettingsListView(ListView):
    model = MailingSettings


class MailingSettingsDetailView(DetailView):
    model = MailingSettings


class MailingSettingsCreateView(LoginRequiredMixin, CreateView):
    model = MailingSettings
    fields = ('client', 'start_time', 'end_time', 'periodicity', 'status', 'title', 'text')
    success_url = reverse_lazy('mailings:mailingsettings_list')

    def form_valid(self, form):
        client = form.save()
        mailingsetting = form.save()
        user = self.request.user
        client.owner = user
        mailingsetting.owner = user
        client.save()
        mailingsetting.save()
        return super().form_valid(form)


class MailingSettingsUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingSettings
    success_url = reverse_lazy('mailings:mailingsettings_list')

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return MailingSettingsForm
        if user.has_perm('mailings.view_all_mailings') and user.has_perm('mailings.deactivate_mailing'):
            return ModeratorMailingSettingsForm
        raise PermissionDenied


class MailingSettingsDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingSettings
    success_url = reverse_lazy('mailings:mailingsettings_list')


class LogListView(ListView):
    model = Log

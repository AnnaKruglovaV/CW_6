from django.contrib import admin

from mailings.models import Client, MailingSettings, Log, Message


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'comment',)
    list_filter = ('name', 'email',)


@admin.register(MailingSettings)
class MailingSettingsAdmin(admin.ModelAdmin):
    list_display = ('title', 'periodicity', 'status', 'owner')
    list_filter = ('client', 'title',)
    list_display_links = ('title', 'periodicity', 'status')


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('time', 'status', 'server_response', 'mailing_list', 'client',)
    list_filter = ('status', 'server_response', 'client',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'text')
    search_fields = ('subject',)

from django import forms

from mailings.models import MailingSettings
from users.forms import StyleFormMixin


class MailingSettingsForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailingSettings
        exclude = ('owner',)


class ModeratorMailingSettingsForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailingSettings
        fields = ('status',)

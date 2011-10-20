from django import forms

from .models import SimpleModel, ChoiceModel, ReleatedModel


class SimpleModelForm(forms.ModelForm):
    class Meta:
        model = SimpleModel


class ChoiceModelForm(forms.ModelForm):
    class Meta:
        model = ChoiceModel


class ReleatedModelForm(forms.ModelForm):
    class Meta:
        model = ReleatedModel


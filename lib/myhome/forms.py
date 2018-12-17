from django.forms import ModelForm

from myhome import models


class ZoneForm(ModelForm):
    class Meta:
        model = models.Zone
        fields = '__all__'


class ScriptForm(ModelForm):
    class Meta:
        model = models.Script
        fields = '__all__'

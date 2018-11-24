from django.forms import ModelForm

from myhome import models


class ZoneForm(ModelForm):
    class Meta:
        model = models.Zone
        fields = '__all__'

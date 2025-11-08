from django import forms
from .models import Court, OpeningHour, Block

class CourtForm(forms.ModelForm):
    class Meta:
        model = Court
        fields = ["name","court_type","price_per_hour","is_active"]

class OpeningHourForm(forms.ModelForm):
    class Meta:
        model = OpeningHour
        fields = ["court","weekday","start_time","end_time"]

class BlockForm(forms.ModelForm):
    class Meta:
        model = Block
        fields = ["court","start","end","reason"]

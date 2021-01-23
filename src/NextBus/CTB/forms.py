from django import forms

class RouteForm(forms.Form):
    search_route = forms.CharField(label='Route', max_length=10)
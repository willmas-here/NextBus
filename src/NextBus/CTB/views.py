from django.shortcuts import render, HttpResponseRedirect

# Create your views here.
from .updater import update_db

def update_db_view(request):
        update_db()
        return HttpResponseRedirect('/')
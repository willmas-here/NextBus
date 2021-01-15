from django.contrib import admin
from django.urls import path, include

from ctb.views import update_db_view

app_name = 'CTB'
urlpatterns = [
    path('update-db/', update_db_view)
]

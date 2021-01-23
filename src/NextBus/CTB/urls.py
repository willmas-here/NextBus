from django.contrib import admin
from django.urls import path, include

from ctb.views import(
    index_view,
    route_view
)

app_name = 'CTB'
urlpatterns = [
    path('', index_view, name='index'),
    path('<str:route_num>/', route_view, name='route'),
    # path('<str:route>/<int:stop>',)
]

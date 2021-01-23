from django.shortcuts import render, get_object_or_404, redirect

from .models import Route, Stop
from .forms import RouteForm
# Create your views here.
def index_view(request):
    template_name = 'CTB/index.html'
    route_form = RouteForm()

    context = {
        'route_form'    : route_form
    }

    user_route = request.GET.get('search_route', default='')
    if user_route == '':
        return render(request, template_name, context=context)
    else:
        route = Route.objects.get(route=user_route)
        return redirect(route, route_num=user_route)

def route_view(request, route_num):
    route_num = route_num.upper()
    template_name = 'CTB/route.html'
    route = Route.objects.get(route=route_num)

    route_form = RouteForm()
    user_route = request.GET.get('search_route', default='')
    if user_route != '':
        route = Route.objects.get(route=user_route)
        return redirect(route, route_num=user_route)

    route = Route.objects.get(route=route_num)

    # circular routes have no inbound stops
    if route.stops_i != '[]':
        route_stops_i = [int(item.strip("'")) for item in route.stops_i.strip("[]").split(', ')]
        # stops_i = Stop.objects.filter(stop__in=route_stops_i)
        stops_i = [Stop.objects.get(stop=item) for item in route_stops_i]
        circular = False
    else:
        circular = True
        stops_i = None
    

    route_stops_o = [int(item.strip("'")) for item in route.stops_o.strip("[]").split(', ')]
    # stops_o = Stop.objects.filter(stop__in=route_stops_o)
    stops_o = [Stop.objects.get(stop=item) for item in route_stops_o]

    context = {
        'route'         : route,
        'route_form'    : route_form,
        'stops_i'       : stops_i,
        'stops_o'       : stops_o,
        'circular'      : circular,
    }
    return render(request, template_name, context=context)

def stop_view():
    print('stop')
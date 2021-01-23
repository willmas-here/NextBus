from django.shortcuts import render, get_object_or_404, redirect

from .models import Route, Stop
from .forms import RouteForm
from .api import get_eta

# Create your views here.
def index_view(request):
    template_name = 'CTB/index.html'
    route_form = RouteForm()

    context = {
        'route_form'    : route_form
    }

    user_route = request.GET.get('search_route', default='').upper()
    if user_route == '':
        return render(request, template_name, context=context)
    else:
        return redirect('CTB:route', route_num=user_route)

def route_view(request, route_num):
    route_num = route_num.upper()
    template_name = 'CTB/route.html'
    route = Route.objects.get(route=route_num)

    # route search bar
    route_form = RouteForm()
    user_route = request.GET.get('search_route', default='').upper()
    if user_route != '':
        return redirect('CTB:route', route_num=user_route)

    # circular routes have no inbound stops
    if route.stops_i != '[]':
        route_stops_i = [int(item.strip("'")) for item in route.stops_i.strip("[]").split(', ')]
        stops_i = [Stop.objects.get(stop=item) for item in route_stops_i]
        circular = False
    else:
        circular = True
        stops_i = None
    

    route_stops_o = [int(item.strip("'")) for item in route.stops_o.strip("[]").split(', ')]
    stops_o = [Stop.objects.get(stop=item) for item in route_stops_o]

    context = {
        'route'         : route,
        'route_form'    : route_form,
        'stops_i'       : stops_i,
        'stops_o'       : stops_o,
        'circular'      : circular,
    }
    return render(request, template_name, context=context)

def stop_view(request, route_num, stop_num):
    route_num = route_num.upper()
    template_name = 'CTB/stop.html'

    route = Route.objects.get(route=route_num)
    stop = Stop.objects.get(stop=stop_num)

    # route search bar
    route_form = RouteForm()
    user_route = request.GET.get('search_route', default='').upper()
    if user_route != '':
        return redirect('CTB:route', route_num=user_route)

    # get eta data
    eta_data = get_eta(route.co, str(stop.stop).zfill(6), route.route)
    eta_formatted = []
    has_remark = False
    for seq in eta_data['eta']:
        time = seq['eta'].strftime("%H:%M")
        seq_formatted = seq
        seq_formatted['eta'] = time
        eta_formatted.append(seq_formatted)
        if seq['rmk_en'] != '':
            has_remark = True

    context = {
        'route_form'    : route_form,
        'route'         : route,
        'stop'          : stop,
        'eta_data'      : eta_data,
        'eta_formatted' : eta_formatted,
        'has_remark'    : has_remark,
    }
    return render(request, template_name, context=context)
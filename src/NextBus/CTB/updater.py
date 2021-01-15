import sched, time
from django.core import exceptions

from .api import get_routes, get_route_stop, get_stop
from .models import Route, Stop

new_stops = []

def new_route(route_data):
    local_start = time.time()

    inbound_data = get_route_stop(route_data['co'], route_data['route'], 'inbound')
    outbound_data = get_route_stop(route_data['co'], route_data['route'], 'outbound')

    route = Route(
        co          = route_data['co'],
        route       = route_data['route'],
        orig_tc     = route_data['orig_tc'],
        orig_sc     = route_data['orig_sc'],
        orig_en     = route_data['orig_en'],
        dest_tc     = route_data['dest_tc'],
        dest_sc     = route_data['dest_sc'],
        dest_en     = route_data['dest_en'],
        stops_i     = inbound_data['stops'],
        stops_o     = outbound_data['stops'],
    )
    route.save()

    local_end = time.time()
    local_elapsed = local_end - local_start
    print('Route ' + route_data['route'] + ' added to db.    Time elapsed: ' + str(local_elapsed))

    for stop in inbound_data['stops']:
        if stop not in new_stops:
            new_stops.append(stop)
    
    for stop in outbound_data['stops']:
        if stop not in new_stops:
            new_stops.append(stop)
    
def new_stop(stop_id):
    local_start = time.time()

    stop_data = get_stop(stop_id)
    stop = Stop(
        stop    = stop_id,
        name_tc = stop_data['name_tc'],
        name_sc = stop_data['name_sc'],
        name_en = stop_data['name_en'],
        lat     = stop_data['lat'],
        long    = stop_data['long'],
    )
    stop.save()

    
    local_end = time.time()
    local_elapsed = local_end - local_start
    print('Stop ' + stop_id + ' added to db.    Time elapsed: ' + str(local_elapsed))

def update_db():
    print('Starting update...')
    new_stops.clear()

    delay = 15
    s = sched.scheduler(time.time, time.sleep)

    # add new routes
    route_data = get_routes('ctb')
    for api_route in route_data:
        route_num = api_route['route']
        try:
            db_route = Route.objects.get(route=route_num)
        except exceptions.ObjectDoesNotExist:
            # create new route in db
            s.enter(delay, 5, new_route, argument=(api_route,))
            print(route_num + ' added to api queue')
            continue
        except Exception as e:
            print('route object exception')
            print(e)

        # check route

    print('Starting queue...')
    queue_start = time.time()
    s.run()
    queue_end = time.time()
    queue_elapsed = queue_end - queue_start
    print('Queue complete.  Time Elapsed: ' + str(queue_elapsed))
    
    # add new stops
    for stop in new_stops:
        try:
            db_stop = Stop.objects.get(stop=int(stop))
        except exceptions.ObjectDoesNotExist:
            # create new stop in db
            s.enter(delay, 5, new_stop, argument=(stop,))
            print(stop + ' added to api queue')
            continue
        except Exception as e:
            print('stop object error  ', e)

        # check stop

    print('Starting queue...')
    queue_start = time.time()
    s.run()
    queue_end = time.time()
    queue_elapsed = queue_end - queue_start
    print('Queue complete.  Time Elapsed: ' + str(queue_elapsed))
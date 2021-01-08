import requests
import datetime

def get_route_stop(company, route, direction='outbound'):
    url = 'https://rt.data.gov.hk/v1/transport/citybus-nwfb/route-stop/{company}/{route}/{direction}'
    resp = requests.get(url.format(company=company, route=route, direction=direction)).json()

    route_data = {
        'co'    : resp['data'][0]['co'],
        'route' : resp['data'][0]['route'],
        'dir'   : resp['data'][0]['dir'],
        'stops' : [stop['stop'] for stop in resp['data']]
    }
    return route_data

def get_stop(stop_id):
    url = 'https://rt.data.gov.hk/v1/transport/citybus-nwfb/stop/{stop_id}'
    resp = requests.get(url.format(stop_id=stop_id)).json()

    stop_data = {
        'stop'      : resp['data']['stop'],
        'name_tc'   : resp['data']['name_tc'],
        'name_sc'   : resp['data']['name_sc'],
        'name_en'   : resp['data']['name_en'],
        'lat'       : resp['data']['lat'],
        'long'      : resp['data']['long'],
    }

    return stop_data

def get_eta(company, stop_id, route):
    url = 'https://rt.data.gov.hk/v1/transport/citybus-nwfb/eta/{company}/{stop_id}/{route}'
    resp = requests.get(url.format(company=company, stop_id=stop_id, route=route)).json()

    eta_data = {
        'co'        : resp['data'][0]['co'],
        'route'     : resp['data'][0]['route'],
        'dir'       : resp['data'][0]['dir'],
        'seq'       : resp['data'][0]['seq'],
        'stop'      : resp['data'][0]['stop'],
        'dest_tc'   : resp['data'][0]['dest_tc'],
        'dest_sc'   : resp['data'][0]['dest_sc'],
        'dest_en'   : resp['data'][0]['dest_en'],
        'eta'       : [{
            'eta_seq'   : eta['eta_seq'],
            'eta'       : datetime.datetime.fromisoformat(eta['eta']),
            'rmk_tc'    : eta['rmk_tc'],
            'rmk_sc'    : eta['rmk_sc'],
            'rmk_en'    : eta['rmk_en'],
        } for eta in resp['data']],
    }

    return eta_data

if __name__ == "__main__":
    get_eta('ctb','001025', '12a')
    
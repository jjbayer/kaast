import netifaces


def get_own_ip():

    _, interface = netifaces.gateways()['default'][netifaces.AF_INET]

    return netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']

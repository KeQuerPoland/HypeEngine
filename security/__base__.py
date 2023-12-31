import time
from functools import wraps

import requests
from cachetools import TTLCache
from flask import abort, current_app, jsonify, request
from flask_principal import Identity, PermissionDenied, identity_changed
from ipwhois import IPWhois

from backend import db
from assets.login_handler import current_user
from database.ip_db import IP
from database.parmissions_db import Role
from database.users_db import User
from config import local

website_status = False
app = current_app

VPNAPI_IO_API_KEY = '40f17b0e45764215827bea04a2109423'


def is_proxy_or_vpn(ip):
    cr_usr = current_user()
    try:
        url = f"https://vpnapi.io/api/{ip}?key={VPNAPI_IO_API_KEY}"
        response = requests.get(url)
        data = response.json()

        security = data.get("security", {})
        if security.get("vpn") or security.get("proxy"):
            return True

        return False
    except Exception:
        return False


def save_ip():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            cr_usr = current_user()
            old_ip = request.headers.get(
                'X-Forwarded-For', request.headers.get('X-Real-IP', request.remote_addr))
            ip_address = old_ip.split(',')[0]
            ip = IP.query.filter_by(ip=ip_address).first()
            if ip is None:
                url = f"https://vpnapi.io/api/{ip_address}?key={VPNAPI_IO_API_KEY}"
                response = requests.get(url)
                data = response.json()
                print(data)
                if not local:
                    ip = IP(
                        ip=ip_address,
                        blocked=False,
                        security_vpn=data['security']['vpn'],
                        security_proxy=data['security']['proxy'],
                        security_tor=data['security']['tor'],
                        security_relay=data['security']['relay'],
                        location_city=data['location']['city'],
                        location_region=data['location']['region'],
                        location_country=data['location']['country'],
                        location_continent=data['location']['continent'],
                        location_region_code=data['location']['region_code'],
                        location_country_code=data['location']['country_code'],
                        location_continent_code=data['location']['continent_code'],
                        location_latitude=data['location']['latitude'],
                        location_longitude=data['location']['longitude'],
                        location_time_zone=data['location']['time_zone'],
                        location_locale_code=data['location']['locale_code'],
                        location_metro_code=data['location']['metro_code'],
                        location_is_in_european_union=data['location']['is_in_european_union'],
                        network_network=data['network']['network'],
                        network_autonomous_system_number=data['network']['autonomous_system_number'],
                        network_autonomous_system_organization=data[
                            'network']['autonomous_system_organization']
                    )
                    db.session.add(ip)
                    db.session.commit()

            if cr_usr.is_authenticated:
                cr_usr.save_ip()
                # log.new_log(action="Zapisano IP użytkownika")
            return f(*args, **kwargs)

        return decorated_function
    return decorator


def website_off():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cr_usr = current_user()
            if not website_status:
                if not has_permission('AccessOffline'):
                    return abort(406)

            return func(*args, **kwargs)

        return wrapper
    return decorator


def block_proxy_or_vpn():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cr_usr = current_user()
            old_ip = request.headers.get(
                'X-Forwarded-For', request.headers.get('X-Real-IP', request.remote_addr))
            user_ip = old_ip.split(',')[0]
            with current_app.app_context():
                blocked_ip = IP.query.filter_by(
                    blocked=True).with_entities(IP.ip).all()
                blocked_ip2 = []
                for ip2 in blocked_ip:
                    blocked_ip2.append(ip2[0])

            if user_ip in blocked_ip2:
                # log.new_log(action="Nieautoryzowana próba wejścia",error_message=f"Użytkownik ma nałożoną blokadę i próbował uzyskać dostęp do strony.")
                return abort(406)

            if is_proxy_or_vpn(user_ip):
                # log.new_log(action="Próba wejścia z VPN/PROXY",error_message=f"Użytkownik używa niedozwolonego oprogramowania.")
                return abort(423)

            return func(*args, **kwargs)

        return wrapper

    return decorator


def permission_required(permission_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cr_usr = current_user()
            if not has_permission(permission_name):
                return abort(403)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def roles_required(*role_names):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for role_name in role_names:
                if not has_permission(role_name):
                    abort(403)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def has_permission(permission_name):
    cr_usr = current_user()
    if cr_usr.is_authenticated:
        for role in cr_usr.roles:
            if '*' in [p.name for p in role.permissions]:
                # log.new_log(action="Użytkownik posiada permisje do tej strony")
                return True
            if permission_name in [p.name for p in role.permissions]:
                # log.new_log(action="Użytkownik posiada permisje do tej strony")
                return True
    # log.new_log(action="Użytkownik nie posiada permisji do tej strony")
    return False

from flask import request


def get_ip():
    old_ip = request.headers.get(
        'X-Forwarded-For', request.headers.get('X-Real-IP', request.remote_addr))
    ip_address = old_ip.split(',')[0]
    return ip_address

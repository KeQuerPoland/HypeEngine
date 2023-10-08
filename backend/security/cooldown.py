from flask import current_app, jsonify, Response
from backend.security.get_ip import get_ip
from backend.assets.login_handler import current_user
import time
from backend.database.config_db import Config as cfg

cooldown_cache = {}

def cooldown(response: Response):
    if cfg.get_by_name('COOLDOWN_ENABLED'):
        rate=int(cfg.get_by_name('COOLDOWN_RATE'))
        cr_usr = current_user()
        ip_address = get_ip()

        if ip_address not in cooldown_cache:
            cooldown_cache[ip_address] = {'timestamp': time.time(), 'count': 1}
        else:
            entry = cooldown_cache[ip_address]
                    
            current_time = time.time()
            elapsed_time = current_time - entry['timestamp']
            if elapsed_time > rate:
                entry['timestamp'] = current_time
                entry['count'] = 1
            elif entry['count'] >= rate:
                remaining_time = max(0, int(entry['timestamp'] + rate - current_time))
                response.status_code = 429
                response.data = f"Cooldown in effect, try again in {remaining_time} seconds"
                return response
            else:
                entry['count'] += 1
    return response

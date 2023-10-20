from flask import current_app, jsonify, Response, render_template, request,make_response
from security.get_ip import get_ip
import time
from database.config_db import Config as cfg

cooldown_cache = {}

def cooldown():
    if cfg.get_by_name('COOLDOWN_ENABLED'):
        rate=int(cfg.get_by_name('COOLDOWN_RATE'))
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
                response = make_response(render_template(cfg.get_by_name('COOLDOWN_FILE'), remaining_time=remaining_time))
                response.status_code = 429
                #print(response)
                if current_app.config['DEBUG']:
                    print("SHIELD #1 >> Block")
                return response
            else:
                entry['count'] += 1

from flask import current_app,Response, request
from backend.security.get_ip import get_ip
from termcolor import colored

def page_entry(response: Response):
    method = colored(request.method, 'green')
    endpoint = colored(str(request.path) + " (" + str(request.endpoint) + ")", 'blue')
    status_code = colored(response.status_code, 'yellow' if response.status_code == 200 else 'red')
    ip = colored(get_ip(), 'blue')
    method,status_code,ip,endpoint = str(method),str(status_code),str(ip),str(endpoint)
    current_app.logger.info(f'| %s/%s %s >> %s', method, status_code, ip, endpoint)

    with current_app.app_context():
        from backend.assets.discord_handler import log

        if not request.endpoint == None:
            if request.endpoint != 'static':
                log(f'Page Entry',"#3A94EE")
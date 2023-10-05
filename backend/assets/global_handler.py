from flask import current_app


def get_all_routes():
    output = []
    for rule in current_app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        line = "{:50s} {:20s} {}".format(rule.endpoint, methods, rule)
        output.append(line)
    a = []
    for line in sorted(output):
        a.append(output)
    print(a)

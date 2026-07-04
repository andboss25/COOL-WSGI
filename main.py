from wsgiref.simple_server import make_server
import sys
import os
import json
import importlib.util
import random

global_data = {}

def load_module(file_name, module_name):
    spec = importlib.util.spec_from_file_location(module_name, file_name)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

from script_types import Response
from script_types import Request

def main():
    arguments = sys.argv

    try:
        app_path = sys.argv[1]
    except:
        app_path = "application"

    manifest = json.load(open(os.path.join(
        app_path,
        "manifest.json"
    ),"r"))

    global_data['manifest'] = manifest
    global_data["app_path"] = app_path

    settings = manifest['settings']

    port = settings.get("port",80)
    host = settings.get("host","127.0.0.1")
    debug = settings.get("debug",False)

    with make_server(host, port, app) as httpd:
        print(f"Serving on port {str(port)} and adress {host}..")
        httpd.serve_forever()

def parse_process_string(process_string:str) -> Response:
    process_string = process_string.split("@")
    
    if process_string[0] == "page":
        file = open(
            os.path.join(global_data["app_path"],"pages",process_string[1]),
            "r"
        )

        r = Response()
        r.make_html(file)

        return r
    elif process_string[0] == "script":
        script_path = os.path.join(global_data["app_path"],"scripts",process_string[1])
        module = load_module(script_path,script_path.replace("/",".").replace("\\","."))
        function = module.__dict__[process_string[2]]
        headers = {}
        headers_list = [x for x in global_data["last_environ"] if x.startswith("HTTP_")]
        for g in headers_list:
            headers[g.lstrip("HTTP_")] = global_data["last_environ"][g] # check for anomalies..

        request = Request(
            path= global_data["last_environ"]['PATH_INFO'],
            headers= headers,
            query_string= global_data["last_environ"]['QUERY_STRING'],
            global_data=global_data
        )

        return function(request)
    
    return Response()

def app(environ, start_response):
    views = global_data['manifest']['views']
    autofills = global_data['manifest']['autofill']
    autofills_matches = [autofill for autofill in autofills.keys() if environ['PATH_INFO'].startswith(autofill)]
    global_data["last_environ"] = environ
    if environ['PATH_INFO'] in views.keys():
        process_string = views[environ['PATH_INFO']]
        return_data = parse_process_string(process_string)
        start_response(return_data.status, return_data.headers)
        return return_data.content
    elif any(autofills_matches):
        process_string = autofills[autofills_matches[0]]
        return_data = parse_process_string(process_string)
        start_response(return_data.status, return_data.headers)
        return return_data.content
    else:
        status = "404 Not found"
        headers = [("Content-Type", "text/plain; charset=utf-8")]
        start_response(status, headers)
        return [b"404 not found!"]

if __name__ == "__main__":
    main()

# TODO IMPLEMENT MORE SCRIPT TYPES
# TODO RESTRUCTURE IN A BETTER WAY
# TODO IMPLEMENT DB
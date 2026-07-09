from wsgiref.simple_server import make_server
import sys
import os
import json

global_data = {}

from script_types import Response
from script_types import Request

from core.handle_scripts import compute_prequest_data, compute_postquest_data, load_module
from core.handle_requests import parse_process_string

def main():
    arguments = sys.argv

    global_data['debug'] = False

    try:
        app_path = sys.argv[1]
    except:
        app_path = "application"

    if "--debug" in sys.argv:
        global_data['debug'] = True
    

    manifest = json.load(open(os.path.join(
        app_path,
        "manifest.json"
    ),"r"))

    global_data['manifest'] = manifest
    global_data["app_path"] = app_path

    settings = manifest['settings']

    port = settings.get("port",80)
    host = settings.get("host","127.0.0.1")

    with make_server(host, port, app) as httpd:
        print(f"Serving on port {str(port)} and adress {host}..")
        httpd.serve_forever()

def app(environ, start_response):
    views = global_data['manifest']['views']
    autofills = global_data['manifest']['autofill']
    autofills_matches = [autofill for autofill in autofills.keys() if environ['PATH_INFO'].startswith(autofill)]
    global_data["last_environ"] = environ
    prequest_data = compute_prequest_data(global_data,global_data["last_environ"]['PATH_INFO'])
    if environ['PATH_INFO'] in views.keys():
        process_string = views[environ['PATH_INFO']]
        return_data = parse_process_string(global_data,process_string,prequest_data)
        start_response(return_data.status, return_data.headers)
        return return_data.content
    elif any(autofills_matches):
        process_string = autofills[autofills_matches[0]]
        return_data = parse_process_string(global_data,process_string, prequest_data)
        start_response(return_data.status, return_data.headers)
        return return_data.content
    else:
        r = Response()
        r.status = "404 Not found"
        r.headers = [("Content-Type", "text/plain; charset=utf-8")]
        r.set_content("404 Not found")
        r = compute_postquest_data(global_data,global_data['last_environ']['PATH_INFO'],r)
        start_response(r.status, r.headers)
        return r.content

if __name__ == "__main__":
    main()
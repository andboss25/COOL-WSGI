
import importlib.util
import sys
import os
from script_types import Request

def load_module(file_name, module_name):
    spec = importlib.util.spec_from_file_location(module_name, file_name)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

def compute_postquest_data(global_data,path,response):
    # Shitty coding i know but its a toy library
    for postquest in global_data['manifest']['postquest']:
        if postquest == path or postquest == "*":
            if type( global_data['manifest']['postquest'][postquest] ) == str:
                process_string = global_data['manifest']['postquest'][postquest].split("@")
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
                resp = function(request,response)
                if resp != None:
                    return resp
            else:
                for x in global_data['manifest']['postquest'][postquest]:
                    process_string = x.split("@")
                    script_path = os.path.join(global_data["app_path"],"scripts",process_string[1])
                    module = load_module(script_path,script_path.replace("/",".").replace("\\","."))
                    function = module.__dict__[process_string[2]]
                    headers = {}
                    headers_list = [x for x in global_data["last_environ"] if x.startswith("HTTP_")]
                    for g in headers_list:
                        headers[g.replace("HTTP_","")] = global_data["last_environ"][g]

                    request = Request(
                        path= global_data["last_environ"]['PATH_INFO'],
                        headers= headers,
                        query_string= global_data["last_environ"]['QUERY_STRING'],
                        global_data=global_data
                    )

                    resp = function(request,response)
                    if resp != None:
                        return resp
    
    return response

def compute_prequest_data(global_data,path):
    # Shitty coding i know but its a toy library
    responses = []
    for prequest in global_data['manifest']['prequest']:
        if prequest == path or prequest == "*":
            if type( global_data['manifest']['prequest'][prequest] ) == str:
                process_string = global_data['manifest']['prequest'][prequest].split("@")
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

                responses.append(function(request))
            else:
                for x in global_data['manifest']['prequest'][prequest]:
                    process_string = x.split("@")
                    script_path = os.path.join(global_data["app_path"],"scripts",process_string[1])
                    module = load_module(script_path,script_path.replace("/",".").replace("\\","."))
                    function = module.__dict__[process_string[2]]
                    headers = {}
                    headers_list = [x for x in global_data["last_environ"] if x.startswith("HTTP_")]
                    for g in headers_list:
                        headers[g.replace("HTTP_","")] = global_data["last_environ"][g]

                    request = Request(
                        path= global_data["last_environ"]['PATH_INFO'],
                        headers= headers,
                        query_string= global_data["last_environ"]['QUERY_STRING'],
                        global_data=global_data
                    )

                    responses.append(function(request))

    if len(responses) == 1:
        return responses[0]
    
    if len(responses) == 0:
        return {}

    return responses

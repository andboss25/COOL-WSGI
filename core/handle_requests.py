
import importlib.util
import sys
import os
from script_types import Request,Response
from core.handle_scripts import compute_postquest_data,compute_prequest_data,load_module

def parse_process_string(global_data,process_string:str,prequest_data) -> Response:
    try:
        process_string = process_string.split("@")
        
        if process_string[0] == "page":
            file = open(
                os.path.join(global_data["app_path"],"pages",process_string[1]),
                "r"
            )

            r = Response()
            r.make_html(file)

            return compute_postquest_data(global_data,global_data["last_environ"]['PATH_INFO'],r)
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

            resp = function(request,prequest_data)
            return compute_postquest_data(global_data,request.path,resp)
        
        return Response()
    except Exception as e:
        resp = Response()
        resp.status = "500 Internal Server Error"
        resp.set_content("500 Internal Server Error")

        if global_data['debug']:
            tb = sys.exception().__traceback__
            resp.set_content(f"500 Internal Server Error => {str(e.with_traceback(tb))}")
        
        return compute_postquest_data(global_data,global_data['last_environ']['PATH_INFO'],resp)
    # be carefull here

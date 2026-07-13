
from script_types import Response
from script_types import Request

import os

def http_status_handler(request: Request,response: Response) -> Response:

    if response.status == "404 Not found":
        r = Response()
        r.make_html(
            open(os.path.join(request.global_data['app_path'],"pages","404.html"),"r")
        )
        r.status = "404 Not found"
        return r
    
    if response.status == "500 Internal Server Error":
        if not request.global_data['debug'] :
            r = Response()
            r.make_html(
                open(os.path.join(request.global_data['app_path'],"pages","500.html"),"r")
            )

            r.content[0] = r.content[0].decode().replace("{% last_environ %}",f"").encode()
            r.content[0] = r.content[0].decode().replace("{% error %}","").encode()
            r.status = "500 Internal Server Error"
        else:
            r = Response()
            r.make_html(
                open(os.path.join(request.global_data['app_path'],"pages","500.html"),"r")
            )
            r.content[0] = r.content[0].decode().replace("{% last_environ %}",f"Last environ data: {str(request.global_data['last_environ'])}").encode()
            r.content[0] = r.content[0].decode().replace("{% error %}",response.content[0].decode()).encode()
            
            return response
        return r

    return None 
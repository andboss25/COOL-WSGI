
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
        r = Response()
        r.make_html(
            open(os.path.join(request.global_data['app_path'],"pages","500.html"),"r")
        )
        r.status = "500 Internal Server Error"
        return r

    return None 

from script_types import Response, Request
import datetime

def traffic_logger(request: Request) -> dict:
    file = open("logs\\iplog.txt","a")
    file.write(f"{request.global_data['last_environ']['REMOTE_ADDR']} {str(request.global_data['last_environ']['REQUEST_METHOD'])} {request.global_data['last_environ']['PATH_INFO']}?{request.global_data['last_environ']['QUERY_STRING']} at {str(datetime.datetime.now())} -> {str(request.headers)}\n")
    file.close()
    return { "ip": request.global_data['last_environ']['REMOTE_ADDR']}

def post_traffic_logger(request: Request,response: Response) -> Response:
    file = open("logs\\iplog.txt","a")
    file.write(f"=> Responded with {response.status}\n")
    file.close()
    return None
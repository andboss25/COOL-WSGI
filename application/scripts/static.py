from script_types import Response, Request
import os
import mimetypes

def static(request: Request):
    path_deconstructed = request.path.split("/")
    path_deconstructed.pop(0)
    path_deconstructed.pop(0)
    print(path_deconstructed)
    file_path = os.path.join(
        request.global_data['app_path'],
        "static",
        *path_deconstructed
    )
    print(file_path)
    resp = Response()
    try:
        base_dir = os.path.join(
            request.global_data['app_path'],
            "static"
        )
        print(base_dir)
        requested_path = os.path.relpath(os.path.join(base_dir, file_path))
        print(requested_path)
        if not requested_path.startswith(base_dir):
            resp.set_content("Unauthorized!")
            return resp
        else:
            file = open(file_path,"rb")
            resp.set_content_bytes(file.read())
        resp.headers = [("Content-Type",mimetypes.guess_type(file_path)[0])]
        return resp
        
        # TODO PENTEST
    except FileNotFoundError:
        resp.set_content("404 NOT FOUND")
        resp.status = "404 NOT FOUND"
        return resp
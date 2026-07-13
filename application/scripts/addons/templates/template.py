
from script_types import Response
from script_types import Request

def process_template(request: Request,response: Response) -> Response:

    # DEFAULT VALUES
    request.pass_template_keys({
        "ip":str(request.global_data['last_environ']['REMOTE_ADDR']),
        "test":"<div style='color:black; background-color:white;'><h1>The templating system works!</h1><h2>Remove the {% test %} tag of this page to see the contents...</h2></div>"
    })

    content_type = [header[1] for header in response.headers if header[0] == "Content-Type"][0]
    if content_type == "text/html" or content_type == "text/html;":
        r = response

        for key in request.global_data['keys']:
            r.content[0] = r.content[0].decode().replace("{% " +key+ " %}",str(request.global_data['keys'][key])).encode()

        return r
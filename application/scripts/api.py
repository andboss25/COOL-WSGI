from script_types import Response, Request

def add(request: Request):
    resp = Response()
    resp.set_content("foo")
    if request.quert_dict.get("tuff") == ['true']:
        resp.set_json({
            "tuff":True,
            "i_love_json":True,
        })
    return resp
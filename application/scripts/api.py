from script_types import Response, Request
import logging
import datetime

def add(request: Request,prequest_data:dict):
    resp = Response()
    resp.set_content("foo")
    if request.quert_dict.get("tuff") == ['true']:
        resp.set_json({
            "tuff":True,
            "i_love_json":True,
            "preq":prequest_data
        })
    return resp
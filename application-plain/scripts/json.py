
from script_types import Request

def jsonify(request: Request) -> dict:
    return { "json": request.json()}

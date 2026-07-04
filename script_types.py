
import urllib.parse
import json

global_data : dict

class Request:
    def __init__(self,headers:dict = {},path:str = "",query_string:str = "",global_data : dict = {}):
        self.path = path
        self.headers = headers
        self.quert_dict = urllib.parse.parse_qs(query_string)
        self.global_data = global_data
    
    def fetch_content(self) -> str:
        """Fetch plain body of request and if the body is empty then it will return ''"""
        content_length = self.global_data["last_environ"]['CONTENT_LENGTH']
        if content_length == "":
            return ""
        else:
            content_length = int(content_length)
            content = self.global_data['last_environ']['wsgi.input'].read(content_length)
            return content.decode()
        
    def fetch_content_bytes(self) -> str:
        """Fetch plain body of request and if the body is empty then it will return '' and returns everything in bytes"""
        content_length = self.global_data["last_environ"]['CONTENT_LENGTH']
        if content_length == "":
            return b""
        else:
            content_length = int(content_length)
            content = self.global_data['last_environ']['wsgi.input'].read(content_length)
            return content
        
    def json(self):
        """Returns json object, if the Content-Type is not application/json or the body is empty then it will return and empty dict."""
        content = self.fetch_content()
        if content == "":
            return {}
        elif self.global_data['last_environ']['CONTENT_TYPE'] != "application/json":
            return {}
        else:
            return json.loads(content)
            


class Response:
    def __init__(self):
        self.headers = [("Content-Type", "text/plain; charset=utf-8")]
        self.status = "200 OK"
        self.content = []

    def set_content(self,content: str):
        """Set content of response"""
        self.content = [content.encode()]

    def set_content_bytes(self,content: bytes):
        """Set content of response in bytes"""
        self.content = [content]

    def make_html(self,file):
        """Make the response be html, provide a reader as the file!"""
        self.headers = [("Content-Type", "text/html;")]
        self.set_content(file.read())
    
    def set_json(self,content: dict):
        """Set content of response"""
        self.headers = [("Content-Type", "application/json;")]
        self.set_content(json.dumps(content))
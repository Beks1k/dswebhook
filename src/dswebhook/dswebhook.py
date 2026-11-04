import requests

from exceptions import (
    InvalidURL, SchemaError, AlreadyExists, NoSuchID, 
    ContentTooLarge, ConnectionError, BadRequest, InternalServerError, HTTPError
)
urlr = {}

def init(url:str, id=1):
    '''specify webhook url and id (Deafult 1)'''
    global urlr
    if not url:
        raise InvalidURL(f"MUST BE VALID URL FOR ID {id}")
    if id in urlr:
        raise AlreadyExists(f"{id} ALREADY EXSISTS")
    urlr[id] = url

def send(content:str, ids, statCode:bool=False, flush:bool = False):
    '''Send content to specified webhook'''
    global urlr
    if not urlr:
        raise InvalidURL("FIRST SPECIFY URL USING init(url, id) MODULE")
    if len(content) > 2000:
        raise ContentTooLarge(f"TOO LARGE CONTENT FOR {ids}")
    data = {
        "content":content
    }
    if urlr.get(ids) == None:
        raise NoSuchID(f"NOT FOUND {ids}")
    try:
        a = requests.post(urlr.get(ids), json=data)
    except requests.exceptions.ConnectionError:
        raise ConnectionError(f"CONNECTION ERROR FOR {ids} PLEASE CHECK CONNETCTION AND URL FOR ANY ERRORS")
    except requests.exceptions.MissingSchema:
        raise SchemaError(f"MUST BE WITH https:// OR http:// IF HTTPS NOT SUPPORTED FOR {ids}")
    
    if a.status_code == 400:
        raise BadRequest(f"BAD REQUEST (HTTP ERROR: 400) FOR {ids}")
    
    if a.status_code == 500:
        raise InternalServerError(f"INTERNAL SERVER ERROR (HTTP ERROR: 500) FOR {ids}")

    if not a.ok:
        raise HTTPError(f"SERVER RETURNED NOT 2xx RESPONSE {a.status_code} FOR {ids}")
    
    if statCode:
        print(a.status_code, f"FOR {ids}")

    if flush:
        if a.text == "":
            print(f"NOTHING FROM SERVER FOR {ids}")
        else:
            print(a.text, f"FOR {ids}")
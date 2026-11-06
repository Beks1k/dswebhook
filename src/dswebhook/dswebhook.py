import requests
from expections import(
    BadRequest, InternalServerError, InvalidURL, ContentTooLarge, ConnectionError, 
    SchemaError, NoSuchID, AlreadyExists, HTTPError, TimeOut, UnexpectedError, 
    LimitReached, CantBeEmpty
)

urlr = {}
avurl = {}
username = {}

def init(url:str, id=1, avatarURL=None, user_name=None):
    '''specify webhook url and id (Deafult 1)'''
    global urlr
    global avurl
    global username
    if not url:
        raise InvalidURL(f"MUST BE VALID URL FOR ID {id}")
    if id in urlr:
        raise AlreadyExists(f"{id} ALREADY EXSISTS")
    if avatarURL:
        avurl[id] = avatarURL
    if user_name:
        username[id] = user_name
    urlr[id] = url

def send(content:str, ids, timeout = 10, wavatar=False, wusername=False, statCode:bool=False, flush:bool = False):
    '''Send content to specified webhook'''
    global urlr, avurl, username
    if not urlr:
        raise InvalidURL("FIRST SPECIFY URL USING init(url, id) MODULE")
    if urlr.get(ids) == None:
        raise NoSuchID(f"NOT FOUND {ids}")
    if len(content) > 2000:
        raise ContentTooLarge(f"TOO LARGE CONTENT. FOR {ids}")
    if not content:
        raise CantBeEmpty(f"CONTENT CANT BE EMPTY. FOR {ids}")
    data = {
        "content":content
    }
    if ids in avurl and wavatar:
         data["avatar_url"] = avurl.get(ids)
    if ids in username and wusername:
        data["username"] = username.get(ids)
    try:
        a = requests.post(urlr.get(ids), json=data, timeout=timeout)
    except requests.exceptions.ConnectionError:
        raise ConnectionError(f"CONNECTION ERROR FOR {ids}. PLEASE CHECK CONNETCTION AND URL FOR ANY ERRORS")
    except requests.exceptions.MissingSchema:
        raise SchemaError(f"MUST BE WITH https:// OR http:// IF HTTPS NOT SUPPORTED. FOR {ids}")
    except requests.exceptions.Timeout:
        raise TimeOut(f"TIMED OUT {timeout} SECONDS. FOR {ids}")
    except requests.exceptions.RequestException as e:
        raise UnexpectedError(f"UNEXPECTED ERROR. FOR {ids}")
    if a.status_code == 429:
        raise LimitReached(f"REQUEST LIMIT FOR WEBHOOK REACHED (MAXIMUM 5 TIMES A SECOND). FOR {ids}")
    if a.status_code == 400:
        raise BadRequest(f"BAD REQUEST (HTTP ERROR: 400). FOR {ids}")
    
    if a.status_code == 500:
        raise InternalServerError(f"INTERNAL SERVER ERROR (HTTP ERROR: 500). FOR {ids}")

    if not a.ok:
        raise HTTPError(f"SERVER RETURNED NOT 2xx RESPONSE {a.status_code}. FOR {ids}")
    
    if statCode:
        print(a.status_code, f"FOR {ids}")

    if flush:
        if a.text == "":
            print(f"NOTHING FROM SERVER FOR {ids}")
        else:
            print(a.text, f"FOR {ids}")
    
import requests
from expections import(
    BadRequest, InternalServerError, InvalidURL, ContentTooLarge, ConnectionError, 
    SchemaError, NoSuchID, AlreadyExists, HTTPError, TimeOut, UnexpectedError, 
    LimitReached, CantBeEmpty
)

urlr = {}
avurl = {}
username = {}

def init(url:str, id=1, avatarURL=None, userName=None):
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
    if userName:
        username[id] = userName
    urlr[id] = url

def send(content, ids, timeout = 10, wavatar=False, wusername=False, statCode:bool=False, flush:bool = False):
    '''Send content to specified webhook'''
    global urlr, avurl, username
    if not isinstance(ids, list):
        ids = [ids]
    if not urlr:
        raise InvalidURL("FIRST SPECIFY URL USING init(url, id) MODULE")
    if len(ids) == 0:
        raise CantBeEmpty("LIST CANT BE EMPTY")
    for k in range(0, len(ids)):
        if urlr.get(ids[k]) == None:
            raise NoSuchID(f"NO SUCH ID. ({ids[k]})")

    for i in range(0, len(ids)):
        if len(str(content)) > 2000:
            raise ContentTooLarge(f"TOO LARGE CONTENT. FOR {ids[i]}")
        if not content:
            raise CantBeEmpty(f"CONTENT CANT BE EMPTY. FOR {ids[i]}")
        data = {
            "content":content
        }
        if ids[i] in avurl and wavatar:
            data["avatar_url"] = avurl.get(ids[i])
        if ids[i] in username and wusername:
            data["username"] = username.get(ids[i])
        try:
            a = requests.post(urlr.get(ids[i]), json=data, timeout=timeout)
        except requests.exceptions.ConnectionError:
            raise ConnectionError(f"CONNECTION ERROR FOR {ids[i]}. PLEASE CHECK CONNETCTION AND URL FOR ANY ERRORS")
        except requests.exceptions.MissingSchema:
            raise SchemaError(f"MUST BE WITH https:// OR http:// IF HTTPS NOT SUPPORTED. FOR {ids[i]}")
        except requests.exceptions.Timeout:
            raise TimeOut(f"TIMED OUT {timeout} SECONDS. FOR {ids[i]}")
        except requests.exceptions.RequestException as e:
            raise UnexpectedError(f"UNEXPECTED ERROR. FOR {ids[i]} ({e})")
        if a.status_code == 429:
            raise LimitReached(f"REQUEST LIMIT FOR WEBHOOK REACHED (MAXIMUM 5 TIMES A SECOND). FOR {ids[i]}")
        if a.status_code == 400:
            raise BadRequest(f"BAD REQUEST (HTTP ERROR: 400). FOR {ids[i]}")
    
        if a.status_code == 500:
            raise InternalServerError(f"INTERNAL SERVER ERROR (HTTP ERROR: 500). FOR {ids[i]}")

        if not a.ok:
            raise HTTPError(f"SERVER RETURNED NOT 2xx RESPONSE {a.status_code}. FOR {ids[i]}")
    
        if statCode:
            print(a.status_code, f"FOR {ids[i]}")

        if flush:
            if a.text == "":
                print(f"NOTHING FROM SERVER FOR {ids[i]}")
            else:
                print(a.text, f"FOR {ids[i]}")
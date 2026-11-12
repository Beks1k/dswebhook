class BadRequest(Exception):
    '''When 400 hits in'''
    pass

class InternalServerError(Exception):
    '''When 500 hits in'''
    pass

class InvalidURL(Exception):
    '''When Invalid url is given'''
    pass

class ContentTooLarge(Exception):
    '''When Given content bigger than 2000'''
    pass

class ConnectionError(Exception):
    '''When Connection error accures such as no inter net etc.'''
    pass

class SchemaError(Exception):
    '''When schema not right'''
    pass

class NoSuchID(Exception):
    '''When id is not found in urlr'''
    pass

class AlreadyExists(Exception):
    '''When id is already exists in urlr'''
    pass

class HTTPError(Exception):
    '''When other HTTP error accures'''
    pass

class TimeOut(Exception):
    '''Unexpected Error form requests'''
    pass

class UnexpectedError(Exception):
    '''Unexpected Error form requests'''
    pass

class CantBeEmpty(Exception):
    '''If content is empty'''
    pass

class LimitReached(Exception):
    '''When webhooks limit are reached'''
    pass

class EmptyID(Exception):
    '''When ID is empty'''
    pass
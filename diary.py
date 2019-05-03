import requests
from url_helper import *
from exceptions import *

class Week:
    def __init__(self, session):
        response = session.get(diary_url)

        if 'не найден' in response.text:
            raise LoginError('it appears that you are not logged in')
            
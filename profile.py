import requests
from bs4 import BeautifulSoup
from url_helper import *
from exceptions import *

class Profile:
    def parse_raw(self):
        self.data = {}

        for attr, value in self.raw_data.items():
            if 'Имя' in attr:
                self.name = value.b.string
                self.data['name'] = self.name
            elif 'Логин' in attr:
                self.login = value.b.string
                self.data['login'] = self.login
            elif 'Школа' in attr:
                self.school = value
                self.data['school'] = self.school
            elif 'Должность' in attr:
                self.position = value
                self.data['position'] = self.position


    def __init__(self, session):
        response = session.get(index_url)

        if 'Войти через ЕСИА' in response.text:
            raise LoginError('it appears that you are not logged in')
        
        html = BeautifulSoup(response.text, 'html.parser')
        self.raw_data = {}
        user_table = html.find('table', attrs={'class': 'tableEx'})
        rows = user_table.find_all('tr')
        
        for row in rows:
            cols = row.findAll('td')
            self.raw_data[cols[0]] = cols[1]
        
        self.parse_raw()

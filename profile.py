import requests
from bs4 import BeautifulSoup
from url_helper import *
from exceptions import *

class Profile:
    def parse_raw(self):
        self.data = {}

        for attr, value in self.raw_data.items():
            attr = attr.string
            if 'Имя' in attr:
                self.name = value.b.string
                self.data['name'] = self.name
            elif 'Логин' in attr:
                self.login = value.b.string
                self.data['login'] = self.login
            elif 'Школа' in attr:
                self.school = value.string
                self.data['school'] = self.school
            elif 'Должность' in attr:
                self.position = value.string
                self.data['position'] = self.position
            elif 'рождения' in attr:
                self.birthday = value.string
                self.data['birthday'] = self.birthday
            elif 'Пол' in attr:
                self.gender = value.string
                self.data['gender'] = self.gender
            elif 'Сертификата' in attr:
                self.cert = value.b.string
                self.data['cert'] = self.cert


    def __init__(self, session, data=None):
        if data is not None:
            self.data = data
            self.raw_data = None

            for attr, value in data.items():
                exec('self.{} = {}'.format(attr, value))

            return

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


    def to_str(self):
        return str(self.data)
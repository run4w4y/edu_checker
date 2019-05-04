import requests
from bs4 import BeautifulSoup
from url_helper import *
from exceptions import *
from diary import *


def check_login(f):
    def wrap(self, *args, **kwargs):
        try:
            return f(self, *args, **kwargs)
        except LoginError:
            self.login()
            return f(self, *args, **kwargs)

    return wrap


class Profile:
    def login(self):
        if self.credentials.get('main_password') is None:
            raise CredentialsError('main_pass field is not found')
        elif self.credentials.get('main_login') is None:
            raise CredentialsError('main_login field is not found')

        # first get request to the main page
        headers = {
            'Host': 'edu.tatar.ru',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'close',
            'Upgrade-Insecure-Requests': '1'
        }
        self.session.get(login_url, headers=headers)

        # post login request
        headers = {
            'Host': 'edu.tatar.ru',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'https://edu.tatar.ru/logon',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': '53',
            'Connection': 'close',
            'Cookie': '_ga=GA1.2.1346337607.1556912647; _gid=GA1.2.404413009.1556912647; DNSID=0ac427a828f028ff97208a1dbd362fefbeb1fa06; __utma=146055648.1346337607.1556912647.1556913170.1556913170.1; __utmb=146055648.2.10.1556913170; __utmc=146055648; __utmz=146055648.1556913170.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1',
            'Upgrade-Insecure-Requests': '1'
        }
        self.session.post(login_url, data=self.credentials, headers=headers)

        # get request after login
        headers = {
            'Host': 'edu.tatar.ru',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'https://edu.tatar.ru/logon',
            'Connection': 'close',
            'Cookie': '_ga=GA1.2.1346337607.1556912647; _gid=GA1.2.404413009.1556912647; DNSID=0ac427a828f028ff97208a1dbd362fefbeb1fa06; __utma=146055648.1346337607.1556912647.1556913170.1556913170.1; __utmb=146055648.2.10.1556913170; __utmc=146055648; __utmz=146055648.1556913170.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1',
            'Upgrade-Insecure-Requests': '1'
        }
        self.session.get(login_process_url, headers=headers)

        # finally get the needed data
        response = self.session.get(index_url, headers=headers)

        if 'Неверный логин или пароль' in response.text:
            raise CredentialsError('uncorrect credentials')


    def __init__(self, user):
        self.session = requests.session()
        self.credentials = user

        response = self.session.get(index_url)
        if 'Войти через ЕСИА' in response.text:
            self.login()
            response = self.session.get(index_url)
        
        html = BeautifulSoup(response.text, 'html.parser')
        raw_data = {}
        user_table = html.find('table', attrs={'class': 'tableEx'})
        rows = user_table.find_all('tr')
        
        for row in rows:
            cols = row.findAll('td')
            raw_data[cols[0]] = cols[1]
        
        self.data = {}

        for attr, value in raw_data.items():
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


    @check_login
    def diary_term(self, term=''):
        return DiaryTerm(self.session, term)


    @check_login
    def diary_day(self, date=datetime.today().strftime('%d.%m.%Y')):
        return DiaryDay(self.session, date)


    def __repr__(self):
        return 'instance of Profile class with login {}'.format(self.login)


    def __str__(self):
        return str(self.data)
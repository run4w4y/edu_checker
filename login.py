import requests
from credentials import main_user
from url_helper import *
from exceptions import *

def login(session, user):
    if user.get('main_password') is None:
        raise CredentialsError('main_pass field is not found')
    elif user.get('main_login') is None:
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
    session.get(login_url, headers=headers)

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
    session.post(login_url, data=user, headers=headers)

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
    session.get(login_process_url, headers=headers)

    # finally get the needed data
    return session.get(index_url, headers=headers)


if __name__ == '__main__':
    main_session = requests.session()

    print(login(main_session, main_user).text)
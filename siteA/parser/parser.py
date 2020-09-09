from bs4 import BeautifulSoup
from siteA.models import db, Teams

import requests
import parser_config

URL = parser_config.parse_URL
HEADERS = parser_config.headers_for_parce


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS)
    return r


def get_content(html):
    data = []
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', class_='tourtable')
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
    for dat in data:
        dat.pop(0)

    return data


def add_to_database(tables):#нужно допилить
    for team in tables:
        new_team = Teams(team)
        print(f'Команда {new_team.teamName} найдена')

        if Teams.query.filter_by(teamName=new_team.teamName).exists :
            Teams.teamName = new_team.teamName
            Teams.matchs = new_team.matchs
            Teams.victories = new_team.victories
            Teams.draws = new_team.draws
            Teams.loses = new_team.loses
            Teams.goalsplaus = new_team.goalsplaus
            Teams.points = new_team.points
            print(f'Команда {new_team.teamName} обнавлена в базе данных')
            db.session.commit()

        else:
            db.session.add(new_team)
            db.session.commit()
            print(f'Команда {new_team.teamName} записана в базу данных')


def parse():
    html = get_html(URL)
    print(html)
    if html.status_code == 200:
        add_to_database(get_content(html.text))

    else:
        print('Code not 200')




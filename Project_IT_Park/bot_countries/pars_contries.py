import sqlite3
import requests
from bs4 import BeautifulSoup
url = requests.get('http://ostranah.ru/_lists/capitals.php')
soup = BeautifulSoup(url.text, 'html.parser')

list_counrties = soup.find_all('tr')

def pull_base():
    base_for_bot = sqlite3.connect('countries.db')
    cur = base_for_bot.cursor()
    for i in range(1, len(list_counrties)):
        a = tuple(list_counrties[i].text.strip().split(" "))
        try:
            cur.execute("""INSERT INTO 'countries and capitals'(country, capital) VALUES (?, ?);""", a)
            base_for_bot.commit()
        except sqlite3.ProgrammingError:
            continue


pull_base()
# a = tuple(list_counrties[8].text.strip().split(" "))
# print(a)

